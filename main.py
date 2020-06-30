from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.config import ConfigParser, Config
from kivy.factory import Factory    

from kivy.lang import Builder
from kivy.core.window import Window

from program import *

import threading

Builder.load_file('ui.kv')

class ScrollScreen(Screen):
    _app = ObjectProperty()
    JsonData.getDataFromFile("Settings", "data/settings.json")
    JsonData.getDataFromFile("AppData", "data/appdata.json")
    JsonData.getDataFromFile("CommandsData", "data/commandsdata.json")
    JsonData.get("Settings")["user"]["last_start"] = str(datetime.now())
    JsonData.saveDataToFile("Settings")

    def pronounce(self, text):
        self.speechPronunciation.pronounce(text)
    
    def exec(self):
        self.speechPronunciation = SpeechPronunciation(voiceIndex=0)
        self.speechRecognition = SpeechRecognition(deviceIndex=1)
        self.logger = Logger(pathToFolder="logs/")
        self.appData = JsonData.get("AppData")

        container = self.ids.container

        APP = Program()

        greeting = APP.greetings().split('\n')
        container.add_widget(AnswerTextLabel(text=greeting[0]))
        self.pronounce(greeting[0])

        container.add_widget(AnswerTextLabel(text=greeting[1]))
        self.pronounce(greeting[1])

        while True:
            speech = self.speechRecognition.recognize()
            recognizedText = str(speech["text"]).lower()


            if speech["error"]:
                self.logger.log(speech["text"])
                continue

            else:
                self.logger.log("Recognized text: " + recognizedText)
                container.add_widget(UserTextLabel(text=recognizedText))

            for trash in self.appData["alias"]:
                recognizedText = recognizedText.replace(trash, "")

            for trash in self.appData["tbr"]:
                recognizedText = recognizedText.replace(trash, "")

            # Распознаём и выполняем комманду
            
            answer = APP.executeCommand(CommandRecognition.recognizeCommand(recognizedText))
            container.add_widget(AnswerTextLabel(text=answer))
            self.pronounce(answer)

    def start_thread(self):
        thread = threading.Thread(target=self.exec)
        thread.setDaemon(True)
        thread.start()

class StartMenu(App):
    def __init__(self, **kvargs):
        super(StartMenu, self).__init__(**kvargs)    
        self.config = ConfigParser()
        self.screen_manager = Factory.ManagerScreens()
    def build(self):
        return self.screen_manager
    
class UserTextLabel(Label):
    pass

class AnswerTextLabel(Label):
    pass

class ScrollButton(Button):
    pass

if __name__ == '__main__':
    StartMenu().run()