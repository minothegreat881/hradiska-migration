"""
Integrácia komentárov z XML feedov priamo do HTML článkov
"""

import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime

class CommentIntegrator:
    def __init__(self, mirror_dir: str = "backup/hradiska_mirror"):
        self.mirror_dir = Path(mirror_dir)
        self.stats = {
            'processed': 0,
            'with_comments': 0,
            'total_comments': 0,
            'failed': 0
        }

    def extract_feed_id(self, html_content: str) -> Optional[str]:
        """Extrahuje comment feed ID z HTML článku"""
        match = re.search(
            r'http://www\.hradiska\.sk/feeds/(\d+)/comments/default',
            html_content
        )
        return match.group(1) if match else None

    def load_comments_from_feed(self, feed_id: str) -> List[Dict]:
        """Načíta komentáre z XML feedu"""
        feed_path = self.mirror_dir / "feeds" / feed_id / "comments" / "default.html"

        if not feed_path.exists():
            return []

        try:
            with open(feed_path, 'r', encoding='utf-8') as f:
                content = f.read()

            root = ET.fromstring(content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            comments = []
            entries = root.findall('.//atom:entry', ns)

            for entry in entries:
                author_elem = entry.find('.//atom:author/atom:name', ns)
                content_elem = entry.find('.//atom:content', ns)
                published_elem = entry.find('.//atom:published', ns)

                author = author_elem.text if author_elem is not None else "Anonym"
                comment_html = content_elem.text if content_elem is not None else ""
                published = published_elem.text if published_elem is not None else ""

                # Parsuj dátum
                try:
                    date_obj = datetime.fromisoformat(published.replace('Z', '+00:00'))
                    date_str = date_obj.strftime('%d.%m.%Y %H:%M')
                except:
                    date_str = published[:10] if published else ""

                comments.append({
                    'author': author,
                    'content': comment_html,
                    'date': date_str,
                    'published_iso': published
                })

            # Zoraď od najstarších po najnovšie
            comments.sort(key=lambda x: x['published_iso'])

            return comments

        except Exception as e:
            print(f"  ⚠️  Chyba pri načítaní feedu {feed_id}: {str(e)[:50]}")
            return []

    def generate_comments_html(self, comments: List[Dict]) -> str:
        """Vygeneruje HTML sekciu s komentármi"""

        html = f"""
<!-- KOMENTÁRE PRIDANÉ AUTOMATICKY -->
<div id="comments-section" style="margin: 40px auto; max-width: 800px; padding: 20px; background: #f9f9f9; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
    <h3 style="color: #333; border-bottom: 3px solid #c0a154; padding-bottom: 10px; margin-bottom: 20px; font-family: Georgia, serif;">
        💬 Komentáre ({len(comments)})
    </h3>
"""

        for i, comment in enumerate(comments, 1):
            # Escapuj HTML v mene autora
            author = comment['author'].replace('<', '&lt;').replace('>', '&gt;')

            html += f"""
    <div class="comment" style="background: white; padding: 15px; margin-bottom: 15px; border-left: 4px solid #c0a154; border-radius: 4px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px; color: #666; font-size: 14px;">
            <strong style="color: #c0a154; font-size: 15px;">👤 {author}</strong>
            <span style="color: #999;">📅 {comment['date']}</span>
        </div>
        <div style="color: #333; line-height: 1.6; font-size: 14px;">
            {comment['content']}
        </div>
    </div>
"""

        html += """
</div>
<!-- KONIEC KOMENTÁROV -->
"""
        return html

    def find_insertion_point(self, html_content: str) -> int:
        """Nájde miesto kde vložiť komentáre (pred </body> alebo footer)"""

        # Skús nájsť footer
        footer_match = re.search(r'<footer|<div[^>]*class=["\'][^"\']*footer', html_content, re.IGNORECASE)
        if footer_match:
            return footer_match.start()

        # Ak nie je footer, vlož pred </body>
        body_match = re.search(r'</body>', html_content, re.IGNORECASE)
        if body_match:
            return body_match.start()

        # Ak ani to nie je, vlož na koniec
        return len(html_content)

    def integrate_comments_into_article(self, html_file: Path) -> bool:
        """Integruje komentáre do jedného HTML článku"""

        try:
            # Načítaj HTML
            with open(html_file, 'r', encoding='utf-8') as f:
                html_content = f.read()

            # Skontroluj či už nemá integrované komentáre
            if '<!-- KOMENTÁRE PRIDANÉ AUTOMATICKY -->' in html_content:
                return False  # Už má komentáre

            # Extrahuj feed ID
            feed_id = self.extract_feed_id(html_content)
            if not feed_id:
                return False  # Nemá komentáre

            # Načítaj komentáre
            comments = self.load_comments_from_feed(feed_id)
            if not comments:
                return False  # Prázdny feed

            # Vygeneruj HTML komentárov
            comments_html = self.generate_comments_html(comments)

            # Nájdi miesto na vloženie
            insertion_point = self.find_insertion_point(html_content)

            # Vlož komentáre
            new_html = (
                html_content[:insertion_point] +
                comments_html +
                html_content[insertion_point:]
            )

            # Ulož upravený súbor
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(new_html)

            self.stats['total_comments'] += len(comments)
            return True

        except Exception as e:
            print(f"  ❌ Chyba pri spracovaní {html_file.name}: {str(e)[:50]}")
            self.stats['failed'] += 1
            return False

    def integrate_all_comments(self):
        """Integruje komentáre do všetkých článkov"""

        print("=" * 70)
        print("  INTEGRÁCIA KOMENTÁROV DO HTML ČLÁNKOV")
        print("=" * 70)
        print()

        # Nájdi všetky HTML články (okrem search/label a feeds)
        html_files = []
        for pattern in ['**/*.html']:
            for html_file in self.mirror_dir.glob(pattern):
                # Preskočiť feeds, search, index
                rel_path = str(html_file.relative_to(self.mirror_dir))
                if any(skip in rel_path for skip in ['feeds/', 'search/', 'index.html']):
                    continue
                html_files.append(html_file)

        print(f"📊 Nájdených {len(html_files)} HTML článkov na spracovanie")
        print()
        print("🔄 Integrujem komentáre...")
        print("-" * 70)

        for i, html_file in enumerate(html_files, 1):
            rel_path = html_file.relative_to(self.mirror_dir)

            if i % 10 == 0 or i == 1:
                print(f"[{i}/{len(html_files)}] {rel_path}", end="", flush=True)

            self.stats['processed'] += 1

            if self.integrate_comments_into_article(html_file):
                if i % 10 == 0 or i == 1:
                    print(" ✅ komentáre pridané")
                self.stats['with_comments'] += 1
            else:
                if i % 10 == 0 or i == 1:
                    print()

        print()
        print("=" * 70)
        print("📊 VÝSLEDKY:")
        print("=" * 70)
        print(f"✅ Spracovaných článkov: {self.stats['processed']}")
        print(f"✅ Článkov s komentármi: {self.stats['with_comments']}")
        print(f"✅ Celkový počet komentárov: {self.stats['total_comments']}")
        print(f"❌ Zlyhané: {self.stats['failed']}")
        print("=" * 70)
        print()

        if self.stats['with_comments'] > 0:
            print("🎉 HOTOVO!")
            print()
            print(f"✅ {self.stats['total_comments']} komentárov bolo integrovaných do {self.stats['with_comments']} článkov")
            print()
            print("💡 Komentáre sú teraz súčasťou HTML stránok a zobrazujú sa na konci každého článku.")
            print()
            print("🌐 Spustite lokálny server a pozrite sa:")
            print("   http://localhost:8000")
        else:
            print("⚠️  Žiadne komentáre na integráciu (možno už sú integrované)")

def main():
    import sys
    import io

    # UTF-8 encoding pre Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    integrator = CommentIntegrator()
    integrator.integrate_all_comments()

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
