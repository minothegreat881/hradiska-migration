"""
Konvertor obsahu pre Next.js aplikáciu
Konvertuje stiahnutý HTML obsah na Markdown/MDX formát
"""

import os
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup
import html2text
from typing import Dict, List
from datetime import datetime
import yaml
import shutil

class ContentConverter:
    def __init__(self, backup_dir: str = "../backup", output_dir: str = "../nextjs-app/content"):
        self.backup_dir = Path(backup_dir)
        self.output_dir = Path(output_dir)
        self.content_dir = self.output_dir / "posts"
        self.images_dir = self.output_dir / "images"
        self.data_dir = self.output_dir / "data"

        # Vytvorenie adresárov
        for dir_path in [self.content_dir, self.images_dir, self.data_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)

        # Načítanie metadát
        metadata_file = self.backup_dir / "data" / "metadata.json"
        if metadata_file.exists():
            with open(metadata_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = {}

        # Konfigurácia html2text
        self.h2t = html2text.HTML2Text()
        self.h2t.ignore_links = False
        self.h2t.ignore_images = False
        self.h2t.body_width = 0  # Bez zalamovánia riadkov

    def sanitize_filename(self, title: str) -> str:
        """Vytvorí bezpečné meno súboru z titulku"""
        # Odstránenie diakritiky
        replacements = {
            'á': 'a', 'č': 'c', 'ď': 'd', 'é': 'e', 'í': 'i',
            'ľ': 'l', 'ň': 'n', 'ó': 'o', 'š': 's', 'ť': 't',
            'ú': 'u', 'ý': 'y', 'ž': 'z', 'ô': 'o', 'ä': 'a',
            'Á': 'A', 'Č': 'C', 'Ď': 'D', 'É': 'E', 'Í': 'I',
            'Ľ': 'L', 'Ň': 'N', 'Ó': 'O', 'Š': 'S', 'Ť': 'T',
            'Ú': 'U', 'Ý': 'Y', 'Ž': 'Z', 'Ô': 'O', 'Ä': 'A'
        }

        for sk, en in replacements.items():
            title = title.replace(sk, en)

        # Nahradenie špeciálnych znakov
        filename = re.sub(r'[^\w\s-]', '', title.lower())
        filename = re.sub(r'[-\s]+', '-', filename)
        return filename[:100]  # Max dĺžka 100 znakov

    def extract_article_from_html(self, html_file: Path) -> Dict:
        """Extrahuje článok z HTML súboru"""
        with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, 'html.parser')

        article = {
            'title': '',
            'slug': '',
            'content': '',
            'excerpt': '',
            'date': datetime.now().isoformat(),
            'author': 'hradiska.sk',
            'categories': [],
            'tags': [],
            'images': [],
            'original_url': ''
        }

        # Titulok
        title_elem = soup.find('h1') or soup.find('title')
        if title_elem:
            article['title'] = title_elem.get_text().strip()
            article['slug'] = self.sanitize_filename(article['title'])

        # Obsah článku
        content_elem = None
        for selector in ['.post-content', '.content', '.entry-content',
                        'article', 'main', '#content']:
            content_elem = soup.select_one(selector)
            if content_elem:
                break

        if not content_elem:
            content_elem = soup.find('body')

        if content_elem:
            # Odstránenie navigácie, pätičky atď.
            for elem in content_elem.select('nav, header, footer, .sidebar, .navigation'):
                elem.decompose()

            # Extrakcia obrázkov
            for img in content_elem.find_all('img'):
                img_data = {
                    'src': img.get('src', ''),
                    'alt': img.get('alt', ''),
                    'title': img.get('title', '')
                }
                article['images'].append(img_data)

            # Konverzia na Markdown
            article['content'] = self.h2t.handle(str(content_elem))

            # Vytvorenie výťažku
            text = content_elem.get_text()[:500]
            article['excerpt'] = ' '.join(text.split())[:200] + '...'

        # Dátum
        date_elem = soup.find(['time', '.date', '.post-date'])
        if date_elem:
            date_text = date_elem.get('datetime') or date_elem.get_text()
            # Tu by sme mali parsovať dátum, ale nechám ako je
            article['date'] = date_text or article['date']

        # Kategórie a tagy
        for cat_elem in soup.select('.category, .cat-links a'):
            article['categories'].append(cat_elem.get_text().strip())

        for tag_elem in soup.select('.tag, .tags a'):
            article['tags'].append(tag_elem.get_text().strip())

        return article

    def convert_to_mdx(self, article: Dict) -> str:
        """Konvertuje článok na MDX formát"""
        # Frontmatter
        frontmatter = {
            'title': article['title'],
            'slug': article['slug'],
            'date': article['date'],
            'author': article['author'],
            'excerpt': article['excerpt'],
            'categories': article['categories'],
            'tags': article['tags'],
            'images': article['images']
        }

        mdx_content = f"""---
{yaml.dump(frontmatter, default_flow_style=False, allow_unicode=True)}---

{article['content']}
"""
        return mdx_content

    def process_all_html_files(self):
        """Spracuje všetky HTML súbory"""
        html_dir = self.backup_dir / "html"
        if not html_dir.exists():
            html_dir = self.backup_dir / "wget_backup" / "www.hradiska.sk"

        articles_data = []

        # Nájdenie všetkých HTML súborov
        html_files = list(html_dir.rglob("*.html"))
        print(f"Nájdených {len(html_files)} HTML súborov")

        for i, html_file in enumerate(html_files, 1):
            print(f"Spracovávam {i}/{len(html_files)}: {html_file.name}")

            try:
                # Extrakcia článku
                article = self.extract_article_from_html(html_file)

                if not article['title']:
                    article['title'] = html_file.stem
                    article['slug'] = self.sanitize_filename(html_file.stem)

                # Konverzia na MDX
                mdx_content = self.convert_to_mdx(article)

                # Uloženie MDX súboru
                mdx_filename = f"{article['slug']}.mdx"
                mdx_path = self.content_dir / mdx_filename

                with open(mdx_path, 'w', encoding='utf-8') as f:
                    f.write(mdx_content)

                articles_data.append({
                    'title': article['title'],
                    'slug': article['slug'],
                    'file': mdx_filename,
                    'date': article['date'],
                    'categories': article['categories'],
                    'tags': article['tags']
                })

            except Exception as e:
                print(f"Chyba pri spracovaní {html_file}: {e}")
                continue

        # Uloženie zoznamu článkov
        articles_json = self.data_dir / "articles.json"
        with open(articles_json, 'w', encoding='utf-8') as f:
            json.dump(articles_data, f, ensure_ascii=False, indent=2)

        print(f"Konverzia dokončená! Spracovaných {len(articles_data)} článkov.")

    def copy_assets(self):
        """Skopíruje obrázky a iné assets"""
        # Kopírovanie obrázkov
        src_images = self.backup_dir / "assets" / "images"
        if src_images.exists():
            for img_file in src_images.iterdir():
                if img_file.is_file():
                    shutil.copy2(img_file, self.images_dir)
                    print(f"Skopírovaný obrázok: {img_file.name}")

        # Kopírovanie dokumentov
        src_docs = self.backup_dir / "documents"
        docs_dir = self.output_dir / "documents"
        docs_dir.mkdir(exist_ok=True)

        if src_docs.exists():
            for doc_file in src_docs.iterdir():
                if doc_file.is_file():
                    shutil.copy2(doc_file, docs_dir)
                    print(f"Skopírovaný dokument: {doc_file.name}")

    def generate_navigation_structure(self):
        """Generuje navigačnú štruktúru pre Next.js"""
        navigation = {
            "mainMenu": [
                {"title": "Domov", "href": "/"},
                {"title": "Hradiská", "href": "/hradiska"},
                {"title": "História", "href": "/historia"},
                {"title": "Archeologické nálezy", "href": "/archeologia"},
                {"title": "Mytológia", "href": "/mytologia"},
                {"title": "Mapa", "href": "/mapa"},
                {"title": "Kontakt", "href": "/kontakt"}
            ],
            "categories": [],
            "recentPosts": []
        }

        # Načítanie článkov
        articles_json = self.data_dir / "articles.json"
        if articles_json.exists():
            with open(articles_json, 'r', encoding='utf-8') as f:
                articles = json.load(f)

                # Kategórie
                categories = set()
                for article in articles:
                    categories.update(article.get('categories', []))
                navigation['categories'] = sorted(list(categories))

                # Posledné príspevky
                navigation['recentPosts'] = articles[:10]

        # Uloženie navigácie
        nav_file = self.data_dir / "navigation.json"
        with open(nav_file, 'w', encoding='utf-8') as f:
            json.dump(navigation, f, ensure_ascii=False, indent=2)

        print("Navigačná štruktúra vygenerovaná")

def main():
    """Hlavná funkcia"""
    converter = ContentConverter()

    print("Začínam konverziu obsahu...")
    print("-" * 50)

    # Spracovanie HTML súborov
    converter.process_all_html_files()

    # Kopírovanie assets
    print("\nKopírovanie obrázkov a dokumentov...")
    converter.copy_assets()

    # Generovanie navigácie
    print("\nGenerovanie navigačnej štruktúry...")
    converter.generate_navigation_structure()

    print("\n" + "=" * 50)
    print("Konverzia dokončená!")
    print(f"Obsah je pripravený v: {converter.output_dir}")

if __name__ == "__main__":
    main()