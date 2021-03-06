from imports_and_classes import *
from time import sleep

class ScrollScreen(Screen):
    _app = ObjectProperty()
    threadRunning = NumericProperty(0)
    listening = NumericProperty(1)
    JsonData.getDataFromFile("Settings", "data/settings.json")
    JsonData.getDataFromFile("AppData", "data/appdata.json")
    JsonData.getDataFromFile("CommandsData", "data/commandsdata.json")
    JsonData.get("Settings")["user"]["last_start"] = str(datetime.now())
    JsonData.saveDataToFile("Settings")

    def pronounce(self, text):
        self.speechPronunciation.pronounce(text)
    
    def exec(self):
        self.speechPronunciation = SpeechPronunciation(voiceIndex=0)
        speechRecognition = SpeechRecognition(deviceIndex=1)
        logger = Logger(pathToFolder="logs/")
        appData = JsonData.get("AppData")

        container = self.ids.container

        APP = Program()

        greeting = APP.greetings().split('\n')

        container.add_widget(AnswerTextLabel(text=greeting[0]))
        self.pronounce(greeting[0])

        container.add_widget(AnswerTextLabel(text=greeting[1]))
        self.pronounce(greeting[1])

        while True:
            speech = speechRecognition.recognize()
            recognizedText = str(speech["text"]).lower()

            if speech["error"]:
                logger.log(speech["text"])
                self.listening = 0
                sleep(0.2)
                self.listening = 1
                continue

            else:
                logger.log("Recognized text: " + recognizedText)
                msg = UserTextLabel(text=recognizedText.capitalize())
                container.add_widget(msg)

            for trash in appData["alias"]:
                recognizedText = recognizedText.replace(trash, "")

            for trash in appData["tbr"]:
                recognizedText = recognizedText.replace(trash, "")

            # Распознаём и выполняем комманду
            
            command = CommandRecognition.recognizeCommand(recognizedText)
            answer = APP.executeCommand(command)

            if command['command'] == "music" and answer["music_name"] != None:
                for child in self.children: # for the case if music already plays 
                    if child.id == "music_player":
                        self.remove_widget(child)
                        child.plays(forcedStop = True)
                        child.unload_audio() 
                        
                musicPlayer = MusicPlayer(id="music_player", music_name=answer["music_name"])
                musicPlayer.init_audio()
                self.add_widget(musicPlayer, index=0)

            msg = AnswerTextLabel(text=answer["display"])
            container.add_widget(msg)

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
        popupWindow.open()


class StartMenu(MDApp):
    themeColors = JsonData.get("Settings")["theme_colors"][THEME]
    toolbar_background = themeColors["App"]["toolbar_background"]
    background = themeColors["App"]["background"]

    def __init__(self, **kvargs):
        super(StartMenu, self).__init__(**kvargs)    
        self.config = ConfigParser()
        self.screen_manager = Factory.ManagerScreens()
    
    def build(self):
        #self.theme_cls.theme_style = "Dark"
        self.title = 'Manya'
        return self.screen_manager

    def change_screen(self, screenName):
        self.screen_manager.current = screenName

    def close_music_player(self):
        main_screen = self.screen_manager.screens[1]

        for child in main_screen.children:
            if child.id == "music_player":
                main_screen.remove_widget(child)
                child.plays(forcedStop = True)
                child.unload_audio()
    
if __name__ == '__main__':
    StartMenu().run()