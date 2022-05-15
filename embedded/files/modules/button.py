import machine

class Button:
    def __init__(self, pin, log):
        self.button = machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_DOWN)
        self.value = self.button.value()
        self.log = log
        self.log.info("Value from button: " + str(self.value))

    def is_changed_state(self):
        if self.value != self.button.value():
            self.value = self.button.value()
            self.log.info("Button Pressed!")
            return True
        return False
