from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooser
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.config import ConfigParser, Config
from kivy.factory import Factory    
from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.app import MDApp

from program import *

import threading
import os


class PopupContent(FloatLayout):
    def fill_with_content(self):
        content = self.ids.content
        content.add_widget(PlainTextLabel(text="Для начала - поздоровайтесь с Маней!"))
        content.add_widget(Image(source='data/images/hello.jpg',size_hint_y=None))
        content.add_widget(PlainTextLabel(text="Список всех команд вы можете получить, просто попросив об этом Маню:"))
        content.add_widget(Image(source='data/images/commands.jpg',size_hint_y=None))

        info = self.ids.info
        info.add_widget(PlainTextLabel(text="Маня - часть проекта \"Интегрируемая система голосового управления\".\n Разработка приложения: Ученик \"МОУ Лицей 40\" 11Б класса Шаганов Вячеслав."))


class LoadDialog(FloatLayout):
    def load(self, path, selection):
        musicFolder = path
        JsonData.get("Settings")["user"]["music_folder"] = str(musicFolder)
        JsonData.saveDataToFile("Settings")

class SettingsScreen(Screen):
    def show_load(self):
        self.content = LoadDialog()
        
        self.popup = Popup(title="Load file", content=self.content,
                            size_hint=(0.9, 0.9))
        self.content.ids.closeBtn.bind(on_press = self.popup.dismiss)
        self.content.ids.loadBtn.bind(on_press = self.popup.dismiss)
        self.popup.open()
    
class SettingsItem(Label):
    pass

class UserTextLabel(Label):
    pass

class AnswerTextLabel(Label):
    pass

class ScrollButton(Button):
    pass

class PlainTextLabel(Label):
    pass