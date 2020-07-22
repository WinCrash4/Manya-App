import os, sys
modulesPath = "Modules/"
sys.path.append(os.path.dirname(modulesPath))


from kivy.app import App
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.filechooser import FileChooser
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.config import ConfigParser, Config
from kivy.factory import Factory    
from kivy.core.window import Window
from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, TwoLineIconListItem
from kivymd.uix.toolbar import MDToolbar

from program import *

import threading
import pygame

## PROGRAM SETUP ##

JsonData.getDataFromFile("Settings", "data/settings.json")

THEME = str(JsonData.get("Settings")["user"]["theme"])

Builder.load_file('UI/ui.kv')

pygame.mixer.init()

## CLASSES ##
class PopupContent(FloatLayout):
    def fill_with_content(self):
        content = self.ids.content
        content.add_widget(PlainTextLabel(text="Для начала - поздоровайтесь с Маней!"))
        content.add_widget(Image(source='data/images/hello.jpg', size_hint_y=None))
        content.add_widget(PlainTextLabel(text="Список всех команд вы можете получить, просто попросив об этом Маню:"))
        content.add_widget(Image(source='data/images/commands.jpg', size_hint_y=None))
        content.add_widget(PlainTextLabel(text="В настройках вы можете настроить работу некоторых команд для дальнейшей работы с ними."))
        content.add_widget(Image(source='data/images/settings.jpg', size_hint_y=None))

        info = self.ids.info
        info.add_widget(PlainTextLabel(text="[color=7d7d7d]Маня - часть проекта \"Интегрируемая система голосового управления\".\n\
Разработка приложения: Ученик \"МОУ Лицей 40\" 11Б класса Шаганов Вячеслав.[/color]", markup = True))


class LoadDialog(FloatLayout):
    load_text = StringProperty("Выбрать папку")
    cancel_text = StringProperty("Отмена")

    def load(self, path, selection):
        musicFolder = path
        JsonData.get("Settings")["user"]["music_folder"] = "{}".format(str(musicFolder)+"\\")
        JsonData.saveDataToFile("Settings")

class SettingsScreen(Screen):
    title = StringProperty("Настройки")
    def on_pre_enter(self):
        container = self.ids.container
        SETTINGS_ITEMS = [
            {"text": "Выбрать папку с музыкой",
            "secondaryText": str(JsonData.get("Settings")["user"]["music_folder"]),
            "icon": "folder",
            "action": self.show_load},
            {"text": "Ваше имя",
            "secondaryText": str(JsonData.get("Settings")["user"]["name"]),
            "icon": "account",
            "action": self.change_name},
            {"text": "Цветовая тема",
            "secondaryText": str(JsonData.get("Settings")["user"]["theme"]),
            "icon": "palette-outline",
            "action": self.show_change_theme_popup}
        ]

        if container.children:
            container.clear_widgets()

        for item in SETTINGS_ITEMS:
            text = item["text"]
            secondaryText = item["secondaryText"]
            icon = item["icon"]
            action = item["action"]
            container.add_widget(SettingsItem(text=text, secondaryText=secondaryText, icon=icon, on_release=action))

    def show_load(self, ins):
        content = LoadDialog()
        
        self.popup = Popup(title="Выбрать папку с музыкой", content=content,
                            size_hint=(0.9, 0.9))
        content.ids.closeBtn.bind(on_press = self.popup.dismiss)
        content.ids.loadBtn.bind(on_press = self.popup.dismiss)
        self.popup.open()

    def show_change_theme_popup(self, ins):
        content = ThemeDialog()
        themes = [theme for theme in JsonData.get("Settings")["theme_colors"]]

        for themeName in themes:
            content.ids.container.add_widget(OneLineListItem(text=themeName, on_release=self.change_theme, theme_text_color="Custom",
                                                                    text_color=(1,1,1,1)))
        self.popup = Popup(title="Тема", content=content,
                            size_hint=(0.9, 0.9))
        content.ids.closeBtn.bind(on_press = self.popup.dismiss)
        self.popup.open()

    def change_theme(self, choosenTheme):
        JsonData.get("Settings")["user"]["theme"] = choosenTheme.text
        JsonData.saveDataToFile("Settings")
        self.popup.dismiss
        popup = Popup(title="Вы выбрали тему \"{}\". Изменения вступят в силу после перезапуска приложения".format(choosenTheme.text), 
                            content=FloatLayout(), size_hint=(0.9, None))
        popup.open()

    def change_name(self, ins):
        pass

class ThemeDialog(FloatLayout):
    cancel_text = StringProperty("Отмена")

class MusicPlayer(MDToolbar):
    JsonData.getDataFromFile("Settings", "data/settings.json")

    themeColors = JsonData.get("Settings")["theme_colors"][THEME]
    background = themeColors["App"]["music_player_background"]

    id = StringProperty()
    player_visible = NumericProperty(1)
    music_name = StringProperty()
    player_state = NumericProperty(1)
    music_folder = str(JsonData.get("Settings")["user"]["music_folder"])

    def init_audio(self):
        self.musicModule = pygame.mixer.music
        self.musicModule.load(self.music_folder + self.music_name)
        self.musicModule.play()

    def change_player_state(self):
        self.player_state *= -1
        self.plays()

    def plays(self, forcedStop = False):
        if self.player_state == 1 and not forcedStop:
            self.musicModule.unpause()
        else:
            self.musicModule.pause()

    def unload_audio(self):
        self.musicModule.stop()

class SettingsItem(TwoLineIconListItem):
    icon = StringProperty()
    text = StringProperty()
    secondaryText = StringProperty()

class UserTextLabel(Label):
    themeColors = JsonData.get("Settings")["theme_colors"][THEME]["UserTextLabel"]
    background = themeColors["background"]
    textColor = themeColors["text_color"]

class AnswerTextLabel(Label):
    themeColors = JsonData.get("Settings")["theme_colors"][THEME]["AnswerTextLabel"]
    background = themeColors["background"]
    textColor = themeColors["text_color"]

class ScrollButton(Button):
    pass

class PlainTextLabel(Label):
    pass
