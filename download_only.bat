@echo off
echo ===============================================
echo   HRADISKA.SK - LOKALNE STIAHNUTIE
echo ===============================================
echo.
echo Tento skript stiahne celu stranku lokalne
echo a umozni vam ju spustit offline.
echo.
echo Toto moze trvat 30-60 minut...
echo ===============================================
echo.

REM Kontrola Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python nie je nainstalovany!
    pause
    exit /b 1
)

echo [1/3] Instalacie potrebnych kniznic...
pip install requests beautifulsoup4 lxml

echo.
echo [2/3] Sťahujem webstranku hradiska.sk...
echo (toto moze trvat dlhsie, budete vidiet progress)
echo.

python download_mirror.py

echo.
echo [3/3] Vytvoram spustaci skript...
echo.

REM Vytvorenie spustacieho skriptu
echo @echo off > start_local_server.bat
echo echo Spustam lokalnu kopiu hradiska.sk... >> start_local_server.bat
echo echo. >> start_local_server.bat
echo echo Otvorte prehliadac na: http://localhost:8000 >> start_local_server.bat
echo echo. >> start_local_server.bat
echo echo Pre zastavenie stlacte Ctrl+C >> start_local_server.bat
echo echo. >> start_local_server.bat
echo cd backup\hradiska_mirror >> start_local_server.bat
echo python -m http.server 8000 >> start_local_server.bat

echo.
echo ===============================================
echo   HOTOVO!
echo ===============================================
echo.
echo Stranka je stiahnutá v priecinku: backup\hradiska_mirror
echo.
echo Pre spustenie lokalnej stranky:
echo 1. Spustite: start_local_server.bat
echo 2. Otvorte prehliadac: http://localhost:8000
echo.
echo Vsetky subory su u vas lokalne a funguju offline!
echo.
pause