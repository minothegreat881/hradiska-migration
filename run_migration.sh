#!/bin/bash

echo "==============================================="
echo "   HRADISKA.SK MIGRATION SCRIPT"
echo "==============================================="
echo ""

# Kontrola Python inštalácie
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Python3 nie je nainštalovaný!"
    echo "Prosím nainštalujte Python 3.8+ z https://www.python.org/"
    exit 1
fi

# Kontrola Node.js inštalácie
if ! command -v node &> /dev/null; then
    echo "[ERROR] Node.js nie je nainštalovaný!"
    echo "Prosím nainštalujte Node.js z https://nodejs.org/"
    exit 1
fi

echo "[OK] Python a Node.js sú nainštalované"
echo ""

# Inštalácia Python dependencies
echo "==============================================="
echo "KROK 1: Inštalácia Python knižníc"
echo "==============================================="
pip3 install -r requirements.txt

echo ""
echo "==============================================="
echo "KROK 2: Sťahovanie webstránky"
echo "==============================================="
echo "Toto môže trvať 30-60 minút v závislosti od veľkosti stránky..."
echo ""
cd scripts
python3 scraper.py
cd ..

echo ""
echo "==============================================="
echo "KROK 3: Konverzia obsahu"
echo "==============================================="
cd scripts
python3 converter.py
cd ..

echo ""
echo "==============================================="
echo "KROK 4: Setup Next.js projektu"
echo "==============================================="
cd scripts
python3 setup_nextjs.py
cd ..

echo ""
echo "==============================================="
echo "KROK 5: Export do Word dokumentov"
echo "==============================================="
cd scripts
python3 word_exporter.py
cd ..

echo ""
echo "==============================================="
echo "   MIGRÁCIA DOKONČENÁ!"
echo "==============================================="
echo ""
echo "Výsledky nájdete v:"
echo "- Záloha stránky: backup/"
echo "- Next.js aplikácia: nextjs-app/"
echo "- Word dokumenty: word-export/"
echo ""
echo "Ďalšie kroky:"
echo "1. cd nextjs-app"
echo "2. npm run dev"
echo "3. Otvorte http://localhost:3000"
echo ""