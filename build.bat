set DIST_DIR=dist\bfv-hacker-checker
rmdir /s /q %DIST_DIR%
python set_version.py
pyinstaller --windowed --noconfirm --onefile --icon=res\icon.png --distpath=%DIST_DIR% --name=bfv-hacker-checker main.py
xcopy /s /i /y res %DIST_DIR%\res
xcopy /y config.ini %DIST_DIR%
xcopy /y README.md %DIST_DIR%
mkdir %DIST_DIR%\bin
xcopy /y bin\Tesseract-OCR.zip_part0 %DIST_DIR%\bin
xcopy /y bin\Tesseract-OCR.zip_part1 %DIST_DIR%\bin
xcopy /y bin\Tesseract-OCR.zip_part2 %DIST_DIR%\bin
xcopy /y bin\Tesseract-OCR.zip_part3 %DIST_DIR%\bin
xcopy /y bin\Tesseract-OCR.zip_part4 %DIST_DIR%\bin

