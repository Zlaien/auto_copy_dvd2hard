cd /d "%~dp0"

python main.py stop
python main.py remove
taskkill /f /im pythonservice.exe
pause