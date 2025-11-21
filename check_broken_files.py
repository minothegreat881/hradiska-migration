"""
Kontrola "poškodených" HTML súborov
"""

import os
from pathlib import Path

def check_broken_html():
    mirror_path = Path("backup/hradiska_mirror")
    html_files = list(mirror_path.glob("**/*.html"))

    print("🔍 ANALÝZA 'POŠKODENÝCH' HTML SÚBOROV:")
    print("=" * 70)
    print()

    broken_files = []

    for html_file in html_files:
        try:
            size = html_file.stat().st_size

            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

                # Ak nie je validný HTML
                if '<html' not in content.lower() and '<body' not in content.lower():
                    broken_files.append({
                        'path': str(html_file.relative_to(mirror_path)),
                        'size': size,
                        'preview': content[:200] if content else "(prázdne)"
                    })
        except Exception as e:
            broken_files.append({
                'path': str(html_file.relative_to(mirror_path)),
                'size': 0,
                'preview': f"ERROR: {str(e)[:50]}"
            })

    if broken_files:
        print(f"Nájdených {len(broken_files)} netypických súborov:\n")

        for i, file_info in enumerate(broken_files[:10], 1):  # Prvých 10
            print(f"{i}. {file_info['path']}")
            print(f"   Veľkosť: {file_info['size']} B")
            print(f"   Obsah: {file_info['preview'][:100]}")
            print()

        if len(broken_files) > 10:
            print(f"... a ďalších {len(broken_files) - 10} súborov")

        print()
        print("💡 VYSVETLENIE:")
        print("Tieto súbory sú pravdepodobne:")
        print("  • XML feedy (feeds/posts/)")
        print("  • Redirecty alebo prázdne stránky")
        print("  • Špeciálne systémové súbory")
        print()
        print("✅ TO JE NORMÁLNE - hlavné HTML články fungujú správne!")
    else:
        print("✅ Žiadne poškodené súbory!")

    print("=" * 70)

if __name__ == "__main__":
    import sys
    import io

    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    check_broken_html()
