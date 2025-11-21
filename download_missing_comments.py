"""
Sťahovanie chýbajúcich comment feedov
"""

import re
import requests
from pathlib import Path
from typing import Set
import time

def extract_comment_feed_urls() -> Set[str]:
    """Extrahuje všetky comment feed URLs z HTML článkov"""

    mirror_path = Path("backup/hradiska_mirror")
    html_files = list(mirror_path.glob("**/*.html"))

    comment_feed_urls = set()

    print(f"🔍 Prehľadávam {len(html_files)} HTML súborov...")

    for html_file in html_files:
        try:
            content = html_file.read_text(encoding='utf-8', errors='ignore')

            # Hľadaj všetky comment feed URLs
            # Pattern: http://www.hradiska.sk/feeds/XXXXXXX/comments/default
            matches = re.findall(
                r'http://www\.hradiska\.sk/feeds/(\d+)/comments/default',
                content
            )

            for feed_id in matches:
                url = f"http://www.hradiska.sk/feeds/{feed_id}/comments/default"
                comment_feed_urls.add(url)

        except Exception as e:
            continue

    return comment_feed_urls

def check_existing_feeds() -> Set[str]:
    """Zistí ktoré feedy už máme stiahnuté"""

    mirror_path = Path("backup/hradiska_mirror/feeds")
    existing_ids = set()

    if mirror_path.exists():
        for feed_dir in mirror_path.iterdir():
            if feed_dir.is_dir() and feed_dir.name.isdigit():
                existing_ids.add(feed_dir.name)

    return existing_ids

def download_comment_feed(url: str, feed_id: str) -> bool:
    """Stiahne jeden comment feed"""

    output_path = Path(f"backup/hradiska_mirror/feeds/{feed_id}/comments")
    output_path.mkdir(parents=True, exist_ok=True)

    file_path = output_path / "default.html"

    try:
        response = requests.get(url, timeout=30, verify=False)
        response.raise_for_status()

        with open(file_path, 'wb') as f:
            f.write(response.content)

        return True, response.content

    except Exception as e:
        return False, None

def count_comments_in_feed(content: bytes) -> int:
    """Spočíta komentáre v XML feede"""

    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(content)
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('.//atom:entry', ns)
        return len(entries)
    except:
        return 0

def main():
    import sys
    import io

    # UTF-8 encoding pre Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    # Vypnutie SSL varovaní
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print("=" * 70)
    print("  SŤAHOVANIE CHÝBAJÚCICH COMMENT FEEDOV")
    print("=" * 70)
    print()

    # 1. Nájdi všetky comment feed URLs
    print("📊 Fáza 1: Analýza HTML článkov...")
    all_feed_urls = extract_comment_feed_urls()
    all_feed_ids = {url.split('/')[4] for url in all_feed_urls}

    print(f"✅ Nájdených {len(all_feed_ids)} unikátnych comment feedov v článkoch")
    print()

    # 2. Zisti ktoré už máme
    print("📊 Fáza 2: Kontrola už stiahnutých feedov...")
    existing_ids = check_existing_feeds()

    print(f"✅ Už stiahnutých: {len(existing_ids)} feedov")
    print()

    # 3. Zisti ktoré chýbajú
    missing_ids = all_feed_ids - existing_ids

    print(f"⚠️  Chýba: {len(missing_ids)} comment feedov")
    print()

    if not missing_ids:
        print("✅ Všetky comment feedy už sú stiahnuté!")
        return 0

    # 4. Stiahni chýbajúce
    print("📥 Fáza 3: Sťahovanie chýbajúcich feedov...")
    print("-" * 70)

    total_new_comments = 0
    downloaded = 0
    empty_feeds = 0
    failed = 0

    for i, feed_id in enumerate(sorted(missing_ids), 1):
        url = f"http://www.hradiska.sk/feeds/{feed_id}/comments/default"

        print(f"[{i}/{len(missing_ids)}] Feed {feed_id[:12]}...", end=" ", flush=True)

        success, content = download_comment_feed(url, feed_id)

        if success:
            comment_count = count_comments_in_feed(content)
            if comment_count > 0:
                print(f"✅ {comment_count} komentárov")
                total_new_comments += comment_count
                downloaded += 1
            else:
                print(f"⚪ prázdny")
                empty_feeds += 1
        else:
            print(f"❌ zlyhalo")
            failed += 1

        # Pauza medzi požiadavkami
        time.sleep(0.5)

    print()
    print("=" * 70)
    print("📊 VÝSLEDKY:")
    print("=" * 70)
    print(f"✅ Stiahnuté s komentármi: {downloaded} feedov")
    print(f"⚪ Prázdne feedy: {empty_feeds}")
    print(f"❌ Zlyhané: {failed}")
    print(f"💬 NÁJDENÝCH NOVÝCH KOMENTÁROV: {total_new_comments}")
    print("=" * 70)

    if total_new_comments > 0:
        print()
        print(f"🎉 Našli sme {total_new_comments} dodatočných komentárov!")
        print()
        print("Spustite znova: python analyze_comments.py")
        print("Pre zobrazenie všetkých komentárov.")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
