"""
Web Scraper pre hradiska.sk
Kompletné stiahnutie obsahu webstránky
"""

import os
import time
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from pathlib import Path
import hashlib
import logging
from typing import Set, Dict, List
import concurrent.futures

# Konfigurácia logovania
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class HradiskaScraper:
    def __init__(self, base_url: str = "http://www.hradiska.sk/", output_dir: str = "../backup"):
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.output_dir = Path(output_dir).absolute()
        self.visited_urls: Set[str] = set()
        self.failed_urls: Set[str] = set()
        self.content_map: Dict[str, dict] = {}

        # Vytvorenie adresárovej štruktúry
        self.dirs = {
            'html': self.output_dir / 'html',
            'images': self.output_dir / 'assets' / 'images',
            'css': self.output_dir / 'assets' / 'css',
            'js': self.output_dir / 'assets' / 'js',
            'documents': self.output_dir / 'documents',
            'data': self.output_dir / 'data'
        }

        for dir_path in self.dirs.values():
            dir_path.mkdir(parents=True, exist_ok=True)

        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })

    def get_page_content(self, url: str) -> tuple:
        """Stiahne obsah stránky"""
        try:
            response = self.session.get(url, timeout=30, verify=False)
            response.raise_for_status()
            return response.content, response.headers.get('content-type', '')
        except Exception as e:
            logger.error(f"Chyba pri sťahovaní {url}: {e}")
            self.failed_urls.add(url)
            return None, None

    def save_file(self, content: bytes, url: str, content_type: str) -> str:
        """Uloží súbor na disk"""
        parsed_url = urlparse(url)
        path = parsed_url.path.strip('/')

        # Určenie typu súboru a cieľového adresára
        if 'image' in content_type or path.endswith(('.jpg', '.jpeg', '.png', '.gif', '.svg', '.webp')):
            target_dir = self.dirs['images']
            ext = path.split('.')[-1] if '.' in path else 'jpg'
        elif 'css' in content_type or path.endswith('.css'):
            target_dir = self.dirs['css']
            ext = 'css'
        elif 'javascript' in content_type or path.endswith('.js'):
            target_dir = self.dirs['js']
            ext = 'js'
        elif 'pdf' in content_type or path.endswith('.pdf'):
            target_dir = self.dirs['documents']
            ext = 'pdf'
        else:
            target_dir = self.dirs['html']
            ext = 'html'

        # Generovanie mena súboru
        if path:
            filename = path.replace('/', '_').replace('\\', '_')
            if not filename.endswith(f'.{ext}'):
                filename = f"{filename}.{ext}"
        else:
            hash_name = hashlib.md5(url.encode()).hexdigest()[:10]
            filename = f"index_{hash_name}.{ext}"

        filepath = target_dir / filename

        # Uloženie súboru
        with open(filepath, 'wb') as f:
            f.write(content)

        logger.info(f"Uložený: {filepath}")
        return str(filepath)

    def extract_links(self, html_content: str, base_url: str) -> Set[str]:
        """Extrahuje všetky odkazy zo stránky"""
        soup = BeautifulSoup(html_content, 'html.parser')
        links = set()

        # Odkazy
        for tag in soup.find_all(['a', 'link']):
            href = tag.get('href')
            if href:
                full_url = urljoin(base_url, href)
                if self.domain in urlparse(full_url).netloc:
                    links.add(full_url)

        # Obrázky
        for img in soup.find_all(['img', 'source']):
            src = img.get('src') or img.get('srcset')
            if src:
                # Spracovanie srcset
                if ',' in str(src):
                    for src_item in str(src).split(','):
                        img_url = src_item.strip().split(' ')[0]
                        full_url = urljoin(base_url, img_url)
                        links.add(full_url)
                else:
                    full_url = urljoin(base_url, src)
                    links.add(full_url)

        # Skripty a štýly
        for tag in soup.find_all(['script', 'link']):
            src = tag.get('src') or tag.get('href')
            if src:
                full_url = urljoin(base_url, src)
                if self.domain in urlparse(full_url).netloc or not urlparse(full_url).netloc:
                    links.add(full_url)

        return links

    def parse_article_content(self, html_content: str, url: str) -> dict:
        """Parsuje obsah článku"""
        soup = BeautifulSoup(html_content, 'html.parser')

        article_data = {
            'url': url,
            'title': '',
            'content': '',
            'images': [],
            'date': '',
            'author': '',
            'tags': [],
            'meta': {}
        }

        # Titulok
        title = soup.find('title')
        if title:
            article_data['title'] = title.text.strip()

        h1 = soup.find('h1')
        if h1 and not article_data['title']:
            article_data['title'] = h1.text.strip()

        # Meta tagy
        for meta in soup.find_all('meta'):
            name = meta.get('name') or meta.get('property', '')
            content = meta.get('content', '')
            if name and content:
                article_data['meta'][name] = content

        # Hlavný obsah
        content_div = soup.find('div', class_=['post-content', 'content', 'entry-content', 'article-content'])
        if not content_div:
            content_div = soup.find('article') or soup.find('main')

        if content_div:
            article_data['content'] = content_div.get_text(separator='\n', strip=True)

            # Obrázky v obsahu
            for img in content_div.find_all('img'):
                img_data = {
                    'src': urljoin(url, img.get('src', '')),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                }
                article_data['images'].append(img_data)

        # Dátum
        date_elem = soup.find(['time', 'span', 'div'], class_=['date', 'post-date', 'entry-date'])
        if date_elem:
            article_data['date'] = date_elem.text.strip()

        # Autor
        author_elem = soup.find(['span', 'div', 'a'], class_=['author', 'by', 'post-author'])
        if author_elem:
            article_data['author'] = author_elem.text.strip()

        # Tagy/kategórie
        tags = soup.find_all(['a', 'span'], class_=['tag', 'category', 'label'])
        article_data['tags'] = [tag.text.strip() for tag in tags]

        return article_data

    def crawl_website(self, start_url: str = None, max_pages: int = None):
        """Hlavná funkcia pre crawlovanie celej stránky"""
        start_url = start_url or self.base_url
        to_visit = {start_url}
        page_count = 0

        while to_visit and (max_pages is None or page_count < max_pages):
            url = to_visit.pop()

            if url in self.visited_urls:
                continue

            logger.info(f"Spracovávam: {url}")
            self.visited_urls.add(url)
            page_count += 1

            # Stiahnutie obsahu
            content, content_type = self.get_page_content(url)
            if not content:
                continue

            # Uloženie súboru
            filepath = self.save_file(content, url, content_type)

            # Ak je to HTML, spracuj obsah a nájdi ďalšie odkazy
            if 'html' in content_type or url.endswith('.html'):
                try:
                    html_content = content.decode('utf-8', errors='ignore')

                    # Extrakcia článku
                    article_data = self.parse_article_content(html_content, url)
                    self.content_map[url] = article_data

                    # Extrakcia odkazov
                    new_links = self.extract_links(html_content, url)
                    to_visit.update(new_links - self.visited_urls)

                except Exception as e:
                    logger.error(f"Chyba pri spracovaní HTML {url}: {e}")

            # Pauza medzi požiadavkami
            time.sleep(0.5)

        # Uloženie metadát
        self.save_metadata()

    def save_metadata(self):
        """Uloží metadáta o stiahnutom obsahu"""
        metadata = {
            'base_url': self.base_url,
            'total_pages': len(self.visited_urls),
            'failed_urls': list(self.failed_urls),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'content_map': self.content_map
        }

        metadata_file = self.dirs['data'] / 'metadata.json'
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        # Vytvorenie sitemapy
        sitemap_file = self.dirs['data'] / 'sitemap.txt'
        with open(sitemap_file, 'w', encoding='utf-8') as f:
            for url in sorted(self.visited_urls):
                f.write(f"{url}\n")

        logger.info(f"Metadáta uložené. Stiahnutých stránok: {len(self.visited_urls)}")

    def download_with_wget(self):
        """Alternatívna metóda sťahovania pomocou wget"""
        import subprocess

        wget_command = [
            'wget',
            '--mirror',
            '--convert-links',
            '--adjust-extension',
            '--page-requisites',
            '--no-parent',
            '--directory-prefix=' + str(self.output_dir / 'wget_backup'),
            '--no-check-certificate',
            '--user-agent=Mozilla/5.0',
            '--wait=1',
            '--random-wait',
            self.base_url
        ]

        try:
            subprocess.run(wget_command, check=True)
            logger.info("Wget sťahovanie dokončené")
        except subprocess.CalledProcessError as e:
            logger.error(f"Wget zlyhal: {e}")
        except FileNotFoundError:
            logger.error("Wget nie je nainštalovaný. Použite: apt-get install wget")

def main():
    """Hlavná funkcia"""
    scraper = HradiskaScraper()

    print("Začínam sťahovanie webstránky hradiska.sk...")
    print("Toto môže trvať niekoľko hodín v závislosti od veľkosti stránky.")

    # Pokús sa najprv o wget (kompletnejšie)
    try:
        scraper.download_with_wget()
    except Exception as e:
        logger.warning(f"Wget metóda zlyhala, používam Python scraper: {e}")

    # Python scraper ako záloha
    scraper.crawl_website()

    print(f"\nSťahovanie dokončené!")
    print(f"Stiahnutých stránok: {len(scraper.visited_urls)}")
    print(f"Zlyhané URL: {len(scraper.failed_urls)}")
    print(f"Výstupný adresár: {scraper.output_dir}")

if __name__ == "__main__":
    main()