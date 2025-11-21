@echo off
echo ===============================================
echo   HRADISKA.SK MIGRATION SCRIPT
echo ===============================================
echo.

REM Kontrola Python inštalácie
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python nie je nainštalovaný alebo nie je v PATH!
    echo Prosím nainštalujte Python 3.8+ z https://www.python.org/
    pause
    exit /b 1
)

REM Kontrola Node.js inštalácie
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Node.js nie je nainštalovaný alebo nie je v PATH!
    echo Prosím nainštalujte Node.js z https://nodejs.org/
    pause
    exit /b 1
)

echo [OK] Python a Node.js sú nainštalované
echo.

REM Inštalácia Python dependencies
echo ===============================================
echo KROK 1: Inštalácia Python knižníc
echo ===============================================
pip install beautifulsoup4 scrapy requests wget python-docx html2text markdown pillow pyyaml

echo.
echo ===============================================
echo KROK 2: Sťahovanie webstránky
echo ===============================================
echo Toto môže trvať 30-60 minút v závislosti od veľkosti stránky...
echo.
cd scripts
python scraper.py
cd ..

echo.
echo ===============================================
echo KROK 3: Konverzia obsahu
echo ===============================================
cd scripts
python converter.py
cd ..

echo.
echo ===============================================
echo KROK 4: Setup Next.js projektu
echo ===============================================
cd scripts
python setup_nextjs.py
cd ..

echo.
echo ===============================================
echo KROK 5: Export do Word dokumentov
echo ===============================================
cd scripts
python word_exporter.py
cd ..

echo.
echo ===============================================
echo   MIGRÁCIA DOKONČENÁ!
echo ===============================================
echo.
echo Výsledky nájdete v:
echo - Záloha stránky: backup\
echo - Next.js aplikácia: nextjs-app\
echo - Word dokumenty: word-export\
echo.
echo Ďalšie kroky:
echo 1. cd nextjs-app
echo 2. npm run dev
echo 3. Otvorte http://localhost:3000
echo.
pause