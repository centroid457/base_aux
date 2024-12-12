
REM pyinstaller.exe --onefile --noconsole ../start.py
pyinstaller.exe --clean --distpath ./pyinstaller/dist --workpath ./pyinstaller/build --specpath ./pyinstaller --onefile ./setup.py

