
REM pyinstaller.exe --onefile --noconsole ../start.py


REM you should delete previouse ./pyinstaller/ before starting!

pyinstaller.exe
    --clean
    --contents-directory ./pyinstaller
    --collect-all TESTCASES
    --onefile
    -y
    ./setup.py
