set DIST_DIR=dist\bfv-hacker-checker
rmdir /s /q %DIST_DIR%
rem pyinstaller --noconfirm --windowed --onefile --icon=res\icon.png --distpath=%DIST_DIR% main.py
pyinstaller --noconfirm --windowed --onefile --icon=res\icon.png --distpath=%DIST_DIR% main.py
xcopy /s /i /y res %DIST_DIR%\res
xcopy /y config.ini %DIST_DIR%
mkdir %DIST_DIR%\bin
xcopy /y bin\Tesseract-OCR.zip %DIST_DIR%\bin
