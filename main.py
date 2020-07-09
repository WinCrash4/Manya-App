from imports_and_classes import *

Builder.load_file('ui.kv')

class ScrollScreen(Screen):
    _app = ObjectProperty()
    threadRunning = NumericProperty(0)
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
                container.add_widget(UserTextLabel(text=recognizedText.capitalize()))

            for trash in self.appData["alias"]:
                recognizedText = recognizedText.replace(trash, "")

            for trash in self.appData["tbr"]:
                recognizedText = recognizedText.replace(trash, "")

            # Распознаём и выполняем комманду
            
            answer = APP.executeCommand(CommandRecognition.recognizeCommand(recognizedText))
            container.add_widget(AnswerTextLabel(text=answer["display"]))
            self.pronounce(answer["pronounce"])

    def start_thread(self):
        self.threadRunning = 1
        self.thread = threading.Thread(target=self.exec)
        self.thread.setDaemon(True)
        self.thread.start()

    def get_help(self):
        pattern = PopupContent()
        pattern.fill_with_content()
        popupWindow = Popup(title="Как работать с Маней", content=pattern, size_hint=(0.8, 0.8)) 
        #closeBtn = pattern.ids.close
        #closeBtn.bind(on_press = popupWindow.dismiss)  
        popupWindow.open() # show the popup

    def boom():
        a = 228/0

class StartMenu(MDApp):
    def __init__(self, **kvargs):
        super(StartMenu, self).__init__(**kvargs)    
        self.config = ConfigParser()
        self.screen_manager = Factory.ManagerScreens()
    
    def build(self):
        return self.screen_manager

    def change_screen(self, screenName):
        self.screen_manager.current = screenName
    
if __name__ == '__main__':
    StartMenu().run()