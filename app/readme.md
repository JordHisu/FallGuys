## Run the app on your PC

To run the app, install [Python 3.10](https://www.python.org/).

Then install Kivy (2.1.0 or higher) with all dependencies:

    python -m pip install --upgrade pip setuptools virtualenv
    python -m pip install "kivy[full]"

Finally, run **app/main.py**.


## Run the app on your android

For this step you need to use Linux or WSL to install buildozer.
If you wish to know how to install WSL, please refer to google.

    git clone https://github.com/kivy/buildozer.git
    cd buildozer
    sudo python setup.py install

Install dependencies:

    sudo apt update
    sudo apt install -y git zip unzip openjdk-13-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
    pip3 install --upgrade Cython==0.29.19 virtualenv

Then add the following line at the end of your <code>~/.bashrc</code> file:
    
    export PATH=$PATH:~/.local/bin/

If there's no <code>buildozer.spec</code> file on the app folder, type <code>buildozer init</code> to create it.
You can configure your build with this file.
Now you can build the application.

    buildozer -v android debug

The apk will be on the <code>app/bin</code> folder. If compiled successfully, you can install it on your phone.
An easy way is to transfer the apk through whatsapp web and download it in your phone.
You can also build and run the app on a connected device, but this is a little complicated.
I will let useful links down below that you can use as a reference if you wish to try that.
Please don't waste too much time.

[Install adb and configure your phone (with download links)](https://www.xda-developers.com/install-adb-windows-macos-linux/)

[Running the app with buildozer using WSL](https://buildozer.readthedocs.io/en/latest/quickstart.html#run-my-application-from-windows-10)

If you have problems connecting with adb, see the following link: [How to connect your phone with adb using WSL](https://stackoverflow.com/questions/62145379/how-to-connect-android-studio-running-inside-wsl2-with-connected-devices-or-andr)
You must use the same adb version on Windows and WSL.

If everything is configured correctly, you can compile, run and save a log file with errors and prints with the following command:

    buildozer -v android debug deploy run logcat | grep python > ./bin/build_log.txt

Quick reminder to connect adb:
     
    On windows:
    adb devices  <-- you should see a device on the list
    adb tcpip 5555

    On WSL:
    adb devices  <-- you should NOT see devices at this moment
    adb connect PHONE_IP:5555  <-- should connect successfully

    Useful:
    adb kill-server
    adb start-server

