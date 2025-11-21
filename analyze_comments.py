"""
Analýza komentárov z XML feedov
"""

import os
from pathlib import Path
import xml.etree.ElementTree as ET
from collections import defaultdict

def analyze_comments():
    mirror_path = Path("backup/hradiska_mirror")

    print("=" * 70)
    print("  ANALÝZA KOMENTÁROV")
    print("=" * 70)
    print()

    # Nájdi všetky comment feedy
    comment_feeds = list(mirror_path.glob("**/feeds/**/comments/default.html"))

    print(f"📊 Nájdených {len(comment_feeds)} comment feedov\n")

    total_comments = 0
    articles_with_comments = []

    for feed_file in comment_feeds:
        try:
            with open(feed_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parsuj XML
            root = ET.fromstring(content)

            # Namespace pre Atom
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            # Nájdi všetky entry (komentáre)
            entries = root.findall('.//atom:entry', ns)

            if entries:
                # Nájdi title článku (je v feed/title)
                feed_title_elem = root.find('.//atom:title', ns)
                feed_title = feed_title_elem.text if feed_title_elem is not None else "Neznámy článok"

                # Extrahuj komentáre
                comments_data = []
                for entry in entries:
                    author_elem = entry.find('.//atom:author/atom:name', ns)
                    content_elem = entry.find('.//atom:content', ns)
                    published_elem = entry.find('.//atom:published', ns)

                    author = author_elem.text if author_elem is not None else "Anonym"
                    comment_text = content_elem.text if content_elem is not None else ""
                    published = published_elem.text if published_elem is not None else ""

                    comments_data.append({
                        'author': author,
                        'text': comment_text[:100] if comment_text else "",
                        'date': published[:10] if published else ""
                    })

                total_comments += len(entries)

                articles_with_comments.append({
                    'title': feed_title,
                    'count': len(entries),
                    'file': str(feed_file.relative_to(mirror_path)),
                    'comments': comments_data[:3]  # Prvé 3 komentáre
                })

        except Exception as e:
            print(f"⚠️  Chyba pri spracovaní {feed_file.name}: {str(e)[:50]}")

    # Výpis štatistík
    print(f"✅ CELKOVÝ POČET KOMENTÁROV: {total_comments}")
    print(f"✅ Článkov s komentármi: {len(articles_with_comments)}")
    print()

    if articles_with_comments:
        print("📝 UKÁŽKA ČLÁNKOV S KOMENTÁRMI:")
        print("-" * 70)

        # Zoraď podľa počtu komentárov
        articles_with_comments.sort(key=lambda x: x['count'], reverse=True)

        for i, article in enumerate(articles_with_comments[:10], 1):
            print(f"\n{i}. {article['title'][:60]}")
            print(f"   Komentárov: {article['count']}")
            print(f"   Feed: {article['file']}")

            if article['comments']:
                print(f"   Ukážka komentárov:")
                for j, comment in enumerate(article['comments'], 1):
                    author = comment['author']
                    text_preview = comment['text'].replace('\n', ' ')[:80]
                    date = comment['date']
                    print(f"     {j}. {author} ({date}): {text_preview}...")

        if len(articles_with_comments) > 10:
            print(f"\n... a ďalších {len(articles_with_comments) - 10} článkov s komentármi")

    print()
    print("=" * 70)
    print("📋 ZÁVER:")
    print("=" * 70)

    if total_comments > 0:
        print(f"✅ Máte {total_comments} komentárov z {len(articles_with_comments)} článkov!")
        print()
        print("💡 Komentáre sú uložené v XML formáte.")
        print("   Ak budete chcieť:")
        print("   • Zobraziť ich v HTML - treba ich integrovať do článkov")
        print("   • Exportovať do Word - môžeme to spraviť")
        print("   • Archivovať - už sú bezpečne uložené")
    else:
        print("⚠️  Nenašli sa žiadne komentáre v XML feedoch")
        print("   (Možno stránka nemá verejné komentáre)")

    print("=" * 70)

if __name__ == "__main__":
    import sys
    import io

    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    analyze_comments()
