set DIST_DIR=dist\bfv-hacker-checker
pyinstaller --noconfirm --windowed --onefile --icon=res\icon.png --distpath=%DIST_DIR% main.py
xcopy /s /i /y res %DIST_DIR%\res
xcopy /y config.ini %DIST_DIR%