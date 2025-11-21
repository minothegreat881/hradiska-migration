"""
Verifikačný skript pre kontrolu inštalácie
"""

import sys
import subprocess
import importlib
from pathlib import Path

def check_python():
    """Kontrola Python verzie"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Potrebná verzia 3.8+")
        return False

def check_node():
    """Kontrola Node.js inštalácie"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ Node.js {version} - OK")
        return True
    except FileNotFoundError:
        print("❌ Node.js nie je nainštalovaný")
        return False

def check_python_packages():
    """Kontrola Python knižníc"""
    packages = [
        'bs4',
        'scrapy',
        'requests',
        'wget',
        'docx',
        'html2text',
        'markdown',
        'PIL',
        'yaml'
    ]

    all_installed = True
    for package in packages:
        try:
            if package == 'bs4':
                importlib.import_module('bs4')
            elif package == 'PIL':
                importlib.import_module('PIL')
            else:
                importlib.import_module(package)
            print(f"✅ {package} - nainštalovaný")
        except ImportError:
            print(f"❌ {package} - chýba")
            all_installed = False

    return all_installed

def check_directories():
    """Kontrola štruktúry priečinkov"""
    dirs = [
        'scripts',
        'backup',
        'nextjs-app',
        'word-export'
    ]

    all_exist = True
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"✅ {dir_name}/ - existuje")
        else:
            print(f"⚠️  {dir_name}/ - neexistuje (bude vytvorený)")

    return True

def check_scripts():
    """Kontrola existencie skriptov"""
    scripts = [
        'scripts/scraper.py',
        'scripts/converter.py',
        'scripts/setup_nextjs.py',
        'scripts/word_exporter.py',
        'run_migration.bat',
        'run_migration.sh'
    ]

    all_exist = True
    for script in scripts:
        if Path(script).exists():
            print(f"✅ {script} - existuje")
        else:
            print(f"❌ {script} - chýba")
            all_exist = False

    return all_exist

def check_git():
    """Kontrola Git inštalácie"""
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"✅ {version} - OK")
        return True
    except FileNotFoundError:
        print("⚠️  Git nie je nainštalovaný (potrebný pre deployment)")
        return True  # Nie je kritický

def main():
    print("=" * 50)
    print("VERIFIKÁCIA INŠTALÁCIE")
    print("=" * 50)
    print()

    results = []

    print("1. Kontrola Python:")
    results.append(check_python())
    print()

    print("2. Kontrola Node.js:")
    results.append(check_node())
    print()

    print("3. Kontrola Python knižníc:")
    results.append(check_python_packages())
    print()

    print("4. Kontrola priečinkov:")
    check_directories()
    print()

    print("5. Kontrola skriptov:")
    results.append(check_scripts())
    print()

    print("6. Kontrola Git:")
    check_git()
    print()

    print("=" * 50)
    if all(results):
        print("✅ VŠETKO JE PRIPRAVENÉ!")
        print("Môžete spustiť migráciu pomocou:")
        print("  Windows: run_migration.bat")
        print("  Linux/Mac: ./run_migration.sh")
    else:
        print("❌ NIEKTORÉ KOMPONENTY CHÝBAJÚ")
        print("Prosím nainštalujte chýbajúce komponenty:")
        print("  Python knižnice: pip install -r requirements.txt")
        print("  Node.js: https://nodejs.org/")
    print("=" * 50)

if __name__ == "__main__":
    main()