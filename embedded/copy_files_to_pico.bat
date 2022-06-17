
:: Use your COM port as an argument while calling this script (ex: copy_files_to_pico.bat COM5)

:: Copy files to Pico
@rshell -p %1 --buffer-size 512 cp -r ./files/ /pyboard/
@rshell cp main.py /pyboard/main.py

:: Run main.py
@rshell repl ~ from main import run ~ run()
