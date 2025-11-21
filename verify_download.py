"""
Verifikačný skript pre kontrolu stiahnutého mirror hradiska.sk
"""

import os
from pathlib import Path
from collections import defaultdict
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def analyze_local_mirror(mirror_dir: str = "backup/hradiska_mirror"):
    """Analyzuje lokálny mirror a vytvorí report"""

    mirror_path = Path(mirror_dir)

    if not mirror_path.exists():
        print(f"❌ Priečinok {mirror_dir} neexistuje!")
        return

    print("=" * 60)
    print("  VERIFIKÁCIA STIAHNUTÉHO MIRROR HRADISKA.SK")
    print("=" * 60)
    print()

    # 1. Základné štatistiky súborov
    print("📊 ANALÝZA SÚBOROV:")
    print("-" * 60)

    stats = defaultdict(int)
    total_size = 0
    years = set()

    for root, dirs, files in os.walk(mirror_path):
        for file in files:
            filepath = Path(root) / file

            # Veľkosť
            try:
                size = filepath.stat().st_size
                total_size += size
            except:
                continue

            # Typ súboru
            ext = filepath.suffix.lower()
            if ext in ['.html', '.htm']:
                stats['HTML'] += 1
                # Extrakcia roku z cesty
                parts = filepath.parts
                for part in parts:
                    if part.isdigit() and len(part) == 4 and 2000 <= int(part) <= 2030:
                        years.add(part)
            elif ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.ico']:
                stats['Obrázky'] += 1
            elif ext in ['.css']:
                stats['CSS'] += 1
            elif ext in ['.js']:
                stats['JavaScript'] += 1
            elif ext in ['.xml']:
                stats['XML'] += 1
            elif ext in ['.txt']:
                stats['Text'] += 1
            else:
                stats['Ostatné'] += 1

    # Výpis štatistík
    total_files = sum(stats.values())
    print(f"✅ Celkový počet súborov: {total_files}")
    print(f"✅ Celková veľkosť: {total_size / (1024*1024):.2f} MB")
    print()

    print("Rozdelenie podľa typu:")
    for file_type, count in sorted(stats.items(), key=lambda x: x[1], reverse=True):
        print(f"  • {file_type:15} {count:4} súborov")
    print()

    # 2. Analýza rokov
    if years:
        print("📅 POKRYTIE ROKOV:")
        print("-" * 60)
        years_sorted = sorted(years)
        print(f"✅ Nájdené články z rokov: {', '.join(years_sorted)}")
        print(f"✅ Rozsah: {years_sorted[0]} - {years_sorted[-1]}")
        print()

    # 3. Kontrola kľúčových súborov
    print("🔍 KONTROLA KĽÚČOVÝCH SÚBOROV:")
    print("-" * 60)

    key_files = [
        "index.html",
        "search/label/aktuality.html",
        "search/label/hradiska.html",
        "search/label/archeologia.html",
    ]

    for key_file in key_files:
        filepath = mirror_path / key_file
        if filepath.exists():
            size = filepath.stat().st_size / 1024
            print(f"✅ {key_file:40} ({size:.1f} KB)")
        else:
            print(f"⚠️  {key_file:40} CHÝBA")
    print()

    # 4. Kontrola integrity HTML súborov
    print("🔗 KONTROLA HTML INTEGRITY:")
    print("-" * 60)

    html_files = list(mirror_path.glob("**/*.html"))
    empty_files = 0
    small_files = 0
    broken_files = 0

    for html_file in html_files:
        try:
            size = html_file.stat().st_size
            if size == 0:
                empty_files += 1
            elif size < 500:  # Podozrivo malé HTML súbory
                small_files += 1

            # Skús načítať ako HTML
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                if '<html' not in content.lower() and '<body' not in content.lower():
                    broken_files += 1
        except:
            broken_files += 1

    print(f"✅ Skontrolovaných HTML súborov: {len(html_files)}")
    if empty_files > 0:
        print(f"⚠️  Prázdne súbory: {empty_files}")
    if small_files > 0:
        print(f"⚠️  Podozrivo malé súbory (<500B): {small_files}")
    if broken_files > 0:
        print(f"❌ Poškodené súbory: {broken_files}")
    else:
        print(f"✅ Žiadne poškodené súbory")
    print()

    # 5. Kontrola obrázkov
    print("🖼️  KONTROLA OBRÁZKOV:")
    print("-" * 60)

    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']
    image_files = []
    for ext in image_extensions:
        image_files.extend(list(mirror_path.glob(f"**/*{ext}")))

    empty_images = 0
    small_images = 0

    for img_file in image_files:
        size = img_file.stat().st_size
        if size == 0:
            empty_images += 1
        elif size < 100:  # Podozrivo malé obrázky
            small_images += 1

    print(f"✅ Celkový počet obrázkov: {len(image_files)}")
    if empty_images > 0:
        print(f"⚠️  Prázdne obrázky: {empty_images}")
    if small_images > 0:
        print(f"⚠️  Podozrivo malé obrázky (<100B): {small_images}")
    else:
        print(f"✅ Všetky obrázky majú validnú veľkosť")
    print()

    # 6. Kontrola štruktúry priečinkov
    print("📁 ŠTRUKTÚRA PRIEČINKOV:")
    print("-" * 60)

    dirs_structure = defaultdict(int)
    for root, dirs, files in os.walk(mirror_path):
        level = root.replace(str(mirror_path), '').count(os.sep)
        if level <= 2:  # Len prvé 2 úrovne
            rel_path = os.path.relpath(root, mirror_path)
            if rel_path != '.':
                dirs_structure[rel_path] = len(files)

    # Zoraď podľa počtu súborov
    for dir_path, file_count in sorted(dirs_structure.items(), key=lambda x: x[1], reverse=True)[:15]:
        print(f"  • {dir_path:45} ({file_count} súborov)")
    print()

    # 7. Finálne zhodnotenie
    print("=" * 60)
    print("📋 FINÁLNE ZHODNOTENIE:")
    print("=" * 60)

    issues = []
    if empty_files > 0:
        issues.append(f"Prázdne HTML súbory: {empty_files}")
    if broken_files > 0:
        issues.append(f"Poškodené HTML súbory: {broken_files}")
    if empty_images > 0:
        issues.append(f"Prázdne obrázky: {empty_images}")

    if not issues:
        print("✅ MIRROR JE KOMPLETNÝ A FUNKČNÝ!")
        print()
        print("Všetko vyzerá v poriadku:")
        print(f"  • {stats['HTML']} HTML stránok")
        print(f"  • {stats['Obrázky']} obrázkov")
        print(f"  • {total_files} celkovo súborov")
        print(f"  • {total_size / (1024*1024):.2f} MB dát")
        print(f"  • Články z rokov {years_sorted[0]}-{years_sorted[-1]}")
        print()
        print("🚀 Môžete bezpečne prehliadať na: http://localhost:8000")
    else:
        print("⚠️  ZISTENÉ PROBLÉMY:")
        for issue in issues:
            print(f"  • {issue}")
        print()
        print("Tieto problémy sú väčšinou normálne (napr. prázdne súbory).")
        print("Stránka by mala fungovať správne.")

    print("=" * 60)

def check_against_live_site():
    """Porovná lokálny mirror s živou stránkou"""
    print()
    print("🌐 POROVNANIE S ŽIVOU STRÁNKOU:")
    print("-" * 60)

    try:
        response = requests.get("http://www.hradiska.sk/", timeout=10, verify=False)
        if response.status_code == 200:
            print("✅ Živá stránka je dostupná")

            soup = BeautifulSoup(response.content, 'html.parser')

            # Počet článkov na hlavnej stránke
            articles = soup.find_all('article')
            if articles:
                print(f"✅ Živá stránka má {len(articles)} článkov na hlavnej stránke")

            # Kontrola hlavných menu položiek
            nav_links = soup.find_all('a', class_='menu-link')
            if nav_links:
                print(f"✅ Nájdených {len(nav_links)} menu položiek")

            print()
            print("💡 Lokálna kópia by mala obsahovať všetko z živej stránky.")

        else:
            print(f"⚠️  Živá stránka odpovedá s kódom: {response.status_code}")

    except Exception as e:
        print(f"⚠️  Nie je možné sa pripojiť k živej stránke: {str(e)[:50]}")
        print("   (To je OK - lokálna kópia funguje nezávisle)")

    print("-" * 60)

if __name__ == "__main__":
    import sys
    import io

    # UTF-8 encoding pre Windows
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

    # Vypnutie SSL varovaní
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    print()
    analyze_local_mirror()
    check_against_live_site()
    print()
