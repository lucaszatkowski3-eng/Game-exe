@echo off

echo Installiere Abhaengigkeiten...
pip install pygame pyinstaller

echo.
echo Erstelle EXE...

pyinstaller --onefile --windowed --name NeonRunner main.py

echo.
echo Fertig!
echo Deine EXE befindet sich jetzt im Ordner "dist".

pause
