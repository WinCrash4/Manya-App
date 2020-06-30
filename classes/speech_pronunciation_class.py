import pyttsx3 as TextToSpeechModule
from classes.logger_class import Logger


class SpeechPronunciation:
    def __init__(self, voiceIndex=4):
        self.engine = TextToSpeechModule.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[voiceIndex].id)

    def pronounce(self, text):
        if Logger.logger:
            Logger.logger.log("Pronounce: " + text)

        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.stop()
