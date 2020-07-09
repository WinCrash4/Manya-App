from classes.json_data_class import JsonData


class CommandRecognition:
    @staticmethod
    def recognizeCommand(recognizedText):
        command = {"command": "", "text": recognizedText}
        matchingWordCount = 0
        isBreak = False

        for cmd, infoAndPhrases in JsonData.get("AppData")["commands"].items():
            if isBreak:
                break

            for phrase in infoAndPhrases[1]:
                if recognizedText.startswith(phrase):
                    command["command"] = cmd
                    isBreak = True
                    break

                for word in phrase.split(' '):
                    if word in recognizedText.split(' '):
                        matchingWordCount += 1

                if matchingWordCount == len(phrase.split(' ')):
                    command["command"] = cmd

                matchingWordCount = 0

        return command
