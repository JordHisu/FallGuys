../rshell/r.py cp -r embedded/files/ /pyboard/
../rshell/r.py cp embedded/main.py /pyboard/main.py

../rshell/r.py repl "~ from main import run ~ run()"