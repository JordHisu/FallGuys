rshell cp -r embedded/files/ /pyboard/
rshell cp embedded/main.py /pyboard/main.py

rshell repl "~ from main import run ~ run()"