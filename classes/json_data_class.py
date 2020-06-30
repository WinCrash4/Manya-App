from json import loads as jsonLoad
from json import dump as jsonDump


class JsonData:
    data = {}
    filePath = {}

    @staticmethod
    def getDataFromFile(name, filePath):
        JsonData.filePath[name] = filePath
        with open(filePath, 'r', encoding="utf-8") as file:
            string = file.read()
            JsonData.data[name] = jsonLoad(string)

        return JsonData.data[name]

    @staticmethod
    def saveDataToFile(name):
        with open(JsonData.filePath[name], 'w', encoding="utf-8") as file:
            jsonDump(JsonData.data[name], file)
            
    @staticmethod
    def get(name):
        return JsonData.data[name]
