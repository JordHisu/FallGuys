import time

class Logger:
    def __init__(self):
        with open("log.txt", "a") as file:
            file.write("\n\nSTART APPLICATION - " + str(time.localtime()) + "\n")
    def info(self, message):
        pass
        # with open("log.txt", "a") as file:
        #     file.write("INFO: " + str(message) + " - " + str(time.localtime()) + "\n")

    def error(self, message):
        pass
        # with open("log.txt", "a") as file:
        #     file.write("ERROR: " + str(message) + " - " + str(time.localtime()) + "\n")
