from datetime import datetime
from classes.json_data_class import JsonData


class Logger:
    logger = None

    def __init__(self, pathToFolder="logs/"):
        startUpData = [
            "   ___  ___    _____    ____   __  __   __  _____  ",
            "  / /\  /\ \  / /_\ \  / /\ \ / / / /__/ / / /_\ \ ",
            " / / / / / / / ___  / / /  \ | /  \_  __/ / ___  / ",
            "/_/ /_/ /_/ /_/  /_/ /_/    \_/    /_/   /_/  /_/  ",
            "                                                  ",
            "Version {}".format(JsonData.get("Settings")["information"]["version"]),
            "",
            "Startup program, please wait..."
        ]
        time = datetime.now()

        self.path = pathToFolder + str(time.date()) + ".log"
        open(self.path, 'a+').close()

        self.log("\nNew loading... Time of load: " + "{}:{}:{} ".format(time.hour, time.minute, time.second) + '\n', printToConsole=False)

        for s in startUpData:
            self.log(s)

        Logger.logger = self

    def log(self, message, printToConsole=True, printToFile=True):
        time = datetime.now()
        message = "[{}:{}:{}] ".format(time.hour, time.minute, time.second) + message

        if printToFile:
            file = open(self.path, 'a')
            file.write(message + '\n')
            file.close()

        if printToConsole:
            print(message)
