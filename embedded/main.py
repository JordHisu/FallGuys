from files.modules.measurements import Measurements


def run():
    measurements = Measurements(stepcallback)
    measurements.start()

steps = 0
def stepcallback():
    global steps
    steps += 1
    print(steps)

if __name__ == "__main__":
    run()