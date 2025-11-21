@echo off
echo ===============================================
echo   HRADISKA.SK - LOKALNY SERVER
echo ===============================================
echo.
echo Spustam lokalnu kopiu stranky...
echo.
echo Otvorte prehliadac na: http://localhost:8000
echo Pre zastavenie stlacte Ctrl+C
echo.
echo ===============================================
cd backup\hradiska_mirror
"C:\Program Files\Python311\python.exe" -m http.server 8000
