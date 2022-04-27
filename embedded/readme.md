
## Basic setup

Before anything, install rshell:

    python -m pip install rshell

## The easy and simple way
To copy your files to Pico and run main.py, you just need to run the following command from the
project's root folder (FallGuys):

    .\embedded\copy_files_to_pico.bat <insert your port here>

    Example:
    .\embedded\copy_files_to_pico.bat COM5

Everything inside the <code>./embedded/files/</code> folder will be copied to Pico, along with main.py from the
<code>./embedded/</code> folder, that will be put on Pico's root.


## The deep and hard way

### Connect to Pico

To connect to the Raspberry Pi Pico, use this command:

    rshell -p <insert your port here> --buffer-size 512

    Example:
    rshell -p COM5 --buffer-size 512

### Copy your files to Pico

Once using rshell, use this command to copy your code to the raspberry:

    cp /embedded/main.py /pyboard/main.py

### Browser Pico's filesystem

If you wish to access the raspberry filesystem, type the following command while using rshell.
This path is a virtual environment created by rshell to access the raspberry filesystem.

    cd /pyboard/

### Run Python code inside Pico

To run the python shell from the raspberry, run the following command while using rshell.
The contents of main.py inside the raspberry filesystem are already loaded at this point.

    repl

Once inside repl, you can just call a function defined on the main.py:
    
    func()

If you wish to run your program automatically, just put it on the main.py body.
It will run on restart. To restart your program after it finishes, you can type ctrl+D on a blank line inside repl.
This will soft reboot your raspberry.

For more information, access https://www.mfitzp.com/using-micropython-raspberry-pico/