
class Logger:
    def __init__(self):
        file=open("log.log","w")
        file.write("START APPLICATION")
        file.close()

    def Info(self, message):
        file = open("log.log", "a")
        file.write("INFO: " + str(message) + "\n")
        file.close()

    def Error(self, message):
        file = open("log.log", "a")
        file.write("ERROR: " + str(message) + "\n")
        file.close()