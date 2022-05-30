# from files.modules.measurements import Measurements

# from files.base import Base
# base = Base()

from files.anklet import Anklet
anklet = Anklet()

def run():
    # base.run()
    anklet.run()
#     measurements = Measurements(stepcallback)
#     measurements.start()

# steps = 0
# def stepcallback():
#     global steps
#     steps += 1
#     print(steps)

if __name__ == "__main__":
    run()