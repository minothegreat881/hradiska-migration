"""
Jednoduchý mirror downloader pre hradiska.sk
Stiahne celú stránku vrátane všetkých súborov pre offline použitie
"""

import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
from typing import Set
import re

class SimpleMirror:
    def __init__(self, base_url: str = "http://www.hradiska.sk/", output_dir: str = "backup/hradiska_mirror"):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self.visited_urls: Set[str] = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

        # Štatistiky
        self.stats = {
            'html': 0,
            'images': 0,
            'css': 0,
            'js': 0,
            'other': 0,
            'failed': 0
        }

    def clean_filename(self, url: str) -> Path:
        """Vytvorí bezpečnú cestu k súboru z URL"""
        import hashlib

        parsed = urlparse(url)
        path = parsed.path

        # Ak je to root, použij index.html
        if not path or path == '/':
            return self.output_dir / 'index.html'

        # Odstránenie úvodného /
        path = path.lstrip('/')

        # Ak cesta končí na /, pridaj index.html
        if path.endswith('/'):
            path += 'index.html'
        elif '.' not in Path(path).name:
            # Ak nemá príponu, pridaj .html
            path += '.html'

        # Nahradenie nebezpečných znakov
        path = path.replace('?', '_').replace('&', '_').replace('=', '_')

        # FIX pre dlhé URL (Windows limit 260 znakov)
        # Ak je cesta príliš dlhá, použij hash
        full_path = self.output_dir / path
        if len(str(full_path)) > 200:  # Bezpečná rezerva
            # Zachovaj príponu
            ext = Path(path).suffix or '.html'
            # Vytvor hash z celej URL
            url_hash = hashlib.md5(url.encode()).hexdigest()[:12]

            # Pre obrázky daj do images/, pre HTML do pages/
            if ext.lower() in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                path = f"images/{url_hash}{ext}"
            elif ext.lower() in ['.css']:
                path = f"css/{url_hash}{ext}"
            elif ext.lower() in ['.js']:
                path = f"js/{url_hash}{ext}"
            else:
                path = f"pages/{url_hash}{ext}"

        return self.output_dir / path

    def download_file(self, url: str) -> bool:
        """Stiahne súbor z URL"""
        try:
            response = self.session.get(url, timeout=30, verify=False)
            response.raise_for_status()

            # Určenie cieľovej cesty
            filepath = self.clean_filename(url)
            filepath.parent.mkdir(parents=True, exist_ok=True)

            # Uloženie súboru
            with open(filepath, 'wb') as f:
                f.write(response.content)

            # Aktualizácia štatistík
            content_type = response.headers.get('content-type', '').lower()
            if 'html' in content_type:
                self.stats['html'] += 1
            elif 'image' in content_type:
                self.stats['images'] += 1
            elif 'css' in content_type:
                self.stats['css'] += 1
            elif 'javascript' in content_type:
                self.stats['js'] += 1
            else:
                self.stats['other'] += 1

            return True, response.content, content_type

        except Exception as e:
            self.stats['failed'] += 1
            print(f"  ❌ Chyba: {str(e)[:50]}")
            return False, None, None

    def get_links_from_html(self, html_content: bytes, base_url: str) -> Set[str]:
        """Extrahuje všetky odkazy z HTML"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            links = set()

            # Stránky
            for tag in soup.find_all('a', href=True):
                href = tag['href']
                full_url = urljoin(base_url, href)
                # Len stránky z rovnakej domény
                if urlparse(full_url).netloc == self.domain:
                    # Odstránenie fragmentov (#)
                    full_url = full_url.split('#')[0]
                    if full_url:
                        links.add(full_url)

            # Obrázky
            for tag in soup.find_all('img', src=True):
                src = tag['src']
                full_url = urljoin(base_url, src)
                links.add(full_url)

            # CSS
            for tag in soup.find_all('link', href=True):
                if tag.get('rel') == ['stylesheet'] or '.css' in tag['href']:
                    href = tag['href']
                    full_url = urljoin(base_url, href)
                    links.add(full_url)

            # JavaScript
            for tag in soup.find_all('script', src=True):
                src = tag['src']
                full_url = urljoin(base_url, src)
                links.add(full_url)

            # Background images z CSS
            for tag in soup.find_all(style=True):
                style = tag['style']
                urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', style)
                for url in urls:
                    full_url = urljoin(base_url, url)
                    links.add(full_url)

            return links

        except Exception as e:
            print(f"  ⚠️  Chyba pri parsovaní HTML: {e}")
            return set()

    def print_progress(self):
        """Zobrazí progress"""
        total = sum([self.stats['html'], self.stats['images'],
                    self.stats['css'], self.stats['js'], self.stats['other']])
        print(f"\r  📊 Stiahnuté: {total} súborov "
              f"(HTML: {self.stats['html']}, "
              f"Obrázky: {self.stats['images']}, "
              f"CSS: {self.stats['css']}, "
              f"JS: {self.stats['js']}, "
              f"Zlyhané: {self.stats['failed']})", end='', flush=True)

    def mirror_website(self, max_pages: int = 1000):
        """Stiahne celú webstránku"""
        print(f"🌐 Začínam sťahovanie: {self.base_url}")
        print(f"📁 Cieľový priečinok: {self.output_dir.absolute()}")
        print()

        to_download = {self.base_url}
        downloaded = 0

        while to_download and downloaded < max_pages:
            url = to_download.pop()

            if url in self.visited_urls:
                continue

            self.visited_urls.add(url)
            downloaded += 1

            # Zobrazenie aktuálneho URL
            short_url = url.replace(self.base_url, '')[:60]
            print(f"\n📥 [{downloaded}/{max_pages}] {short_url}")

            # Stiahnutie
            success, content, content_type = self.download_file(url)

            if success and content and 'html' in (content_type or ''):
                # Extrakcia ďalších odkazov
                new_links = self.get_links_from_html(content, url)
                to_download.update(new_links - self.visited_urls)

            # Progress
            self.print_progress()

            # Pauza medzi požiadavkami
            time.sleep(0.3)

        print("\n")
        print("=" * 50)
        print("✅ SŤAHOVANIE DOKONČENÉ!")
        print("=" * 50)
        print(f"📊 Štatistiky:")
        print(f"  • HTML stránok: {self.stats['html']}")
        print(f"  • Obrázkov: {self.stats['images']}")
        print(f"  • CSS súborov: {self.stats['css']}")
        print(f"  • JS súborov: {self.stats['js']}")
        print(f"  • Ostatných: {self.stats['other']}")
        print(f"  • Zlyhalo: {self.stats['failed']}")
        print(f"  • CELKOM: {sum([self.stats['html'], self.stats['images'], self.stats['css'], self.stats['js'], self.stats['other']])} súborov")
        print()
        print(f"📁 Súbory uložené v: {self.output_dir.absolute()}")

def main():
    """Hlavná funkcia"""
    # Nastavenie UTF-8 encoding pre Windows
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    # Vypnutie SSL varovaní
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print()
    print("=" * 50)
    print("  HRADISKA.SK - MIRROR DOWNLOADER")
    print("=" * 50)
    print()

    mirror = SimpleMirror()

    try:
        mirror.mirror_website(max_pages=1000)

        print()
        print("🚀 ĎALŠIE KROKY:")
        print("1. Spustite: start_local_server.bat")
        print("2. Otvorte prehliadač: http://localhost:8000")
        print()
        print("💡 Všetky súbory sú lokálne a fungujú offline!")

    except KeyboardInterrupt:
        print("\n\n⚠️  Sťahovanie prerušené užívateľom")
        print(f"Stiahnutých {len(mirror.visited_urls)} súborov pred prerušením")
    except Exception as e:
        print(f"\n\n❌ Chyba: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())