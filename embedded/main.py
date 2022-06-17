from files.anklet import Anklet
from files.modules.bluetooth_i2c import Bluetooth
import machine
from files.utils.logger import Logger


def run():
    anklet = Anklet()
    anklet.run()


if __name__ == "__main__":
    run()
