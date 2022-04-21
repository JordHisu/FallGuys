

Install rshell:

    python -m pip install rshell

To connect to the Raspberry Pi Pico, use this command:

    rshell -p <insert you port here> --buffer-size 512

    On my Windows:
    rshell -p COM5 --buffer-size 512

Once using rshell, use this command to copy your code to the raspberry:

    cp /embedded/main.py /pyboard/main.py

If you wish to access the raspberry filesystem, type the following command while using rshell.
This path is a virtual environment created by rshell to access the raspberry filesystem.

    cd /pyboard/

To run the python shell from the raspberry, run the following command while using rshell.
The contents of main.py inside the raspberry filesystem are already loaded at this point.

    repl

Once inside repl, you can just call a function defined on the main.py:
    
    func()

If you wish to run your program automatically, just put it on the main.py body.
It will run on restart. To restart your program after it finishes, you can type ctrl+D on a blank line inside repl.
This will soft reboot your raspberry.

For more information, access https://www.mfitzp.com/using-micropython-raspberry-pico/