set DIST_DIR=dist\bfv-hacker-checker
REM pyinstaller --noconfirm --windowed --onefile --icon=res\icon.png --distpath=%DIST_DIR% main.py
xcopy /s /i /y res %DIST_DIR%\res
xcopy /y config.ini %DIST_DIR%