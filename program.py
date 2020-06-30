# Импортируем классы
from utilities import *

from datetime import datetime
from json import loads as jsonLoad
from googletrans import Translator
from random import randint as randomInteger
from requests import get as getRequest

from classes.logger_class import Logger
from classes.speech_pronunciation_class import SpeechPronunciation
from classes.speech_recognition_class import SpeechRecognition
from classes.command_recognition_class import CommandRecognition
from classes.json_data_class import JsonData

import re           as RegExp
import wikipedia    as Wikipedia
import os           as OS
import random       as Random
import psutil       as PSUtil

class Program:
    def __init__(self):

        Wikipedia.set_lang("ru")

        self.settings = JsonData.get("Settings")
        self.appData = JsonData.get("AppData")
        self.commandsData = JsonData.get("CommandsData")
        self.logger = Logger(pathToFolder="logs/")

        self.loopEnable = True
        self.speechPronunciation = SpeechPronunciation(voiceIndex=0)
        self.speechRecognition = SpeechRecognition(deviceIndex=1)

    def greetings(self):
        greeting = "Приветствую вас, {}".format(str(JsonData.get("Settings")["user"]["name"]))
        phrase = self.chooseRandomPhrase(self.appData["phrases"]["start_message"])
        return greeting + '\n' + phrase

    def chooseRandomPhrase(self, phrases):
        return phrases[randomInteger(0, len(phrases) - 1)]

    def executeCommand(self, commandInfo):
        command = commandInfo["command"]
        recognizedText = commandInfo["text"]

        if command == "hello":
            greetings = self.chooseRandomPhrase(self.appData["phrases"]["greeting"])
            return greetings

        elif command == "ctime":
            time = datetime.now()
            return "Сейчас " + str(time.hour) + ":" + str(time.minute) + ":" + str(time.second) 

        elif command == "music":
            musicIndex = 0
            matchingNamesCount = 0
            matchingWordsCount = 0
            musicDirectory = "E:\Desktop\Мьюзик\\"

            recognizedText = remove_keywords(recognizedText, "music")
            
            if len(recognizedText) != 0: # if the user didn"t say the name of the music
                for index, item in enumerate(OS.listdir(path = musicDirectory)):
                    for word in item.lower()[:-4].split(" "):
                        if word in recognizedText.lower().split(" ")[1:]:
                            matchingWordsCount += 1

                    if matchingWordsCount == len(recognizedText.split(" ")[1:]) and matchingWordsCount != 0:
                        matchingNamesCount += 1
                        musicIndex = index

                        print("[music_found]: " + str(OS.listdir(path = musicDirectory)[index]))

                    matchingWordsCount = 0

                if matchingNamesCount == 0:
                    self.pronounce("Я не нашла музыку с таким названием")

                elif matchingNamesCount == 1:
                    OS.startfile(musicDirectory + OS.listdir(path = musicDirectory)[musicIndex])
                    self.pronounce("Включаю музыку")

                elif matchingNamesCount > 1:
                    self.pronounce("Здесь слишком много песен с таким названием, уточните свой запрос")

                matchingNamesCount = 0

            else:
                musicIndex = Random.randint(0,len(OS.listdir(path = musicDirectory)))
                while OS.listdir(path = musicDirectory)[musicIndex][-4:] != ".mp3":
                    musicIndex = Random.randint(0,len(OS.listdir(path = musicDirectory)))
                self.pronounce("Включаю музыку")
                OS.startfile(musicDirectory + OS.listdir(path = musicDirectory)[musicIndex])

        elif command == "music_disable":
            for pid in (process.pid for process in PSUtil.process_iter() if process.name() == "AIMP.exe"):
                OS.system("taskkill /im  AIMP.exe") # AIMP - name of music player
            self.pronounce("Музыка выключена")

        elif command == "joke":
            jokes = jsonLoad(file.read())["jokes"]
            return self.chooseRandomPhrase(jokes)

        elif command == "thanks":
            thanks = self.appData["phrases"]["thanks"]
            return self.chooseRandomPhrase(thanks)

        elif command == "compliment":
            compliments = self.appData["phrases"]["compliment"]
            return self.chooseRandomPhrase(compliments)

        elif command == "translate":
            textToTranslate = remove_keywords(recognizedText, "translate")
            fromLanguage = "en"
            toLanguage = "ru"

            if "на английский" in textToTranslate or "на английском" in textToTranslate:
                textToTranslate = textToTranslate.replace("на английский", "").replace("на английском", "")
            elif "на русский" in recognizedText or "на русском" in recognizedText:
                recognizedText = recognizedText.replace("на русский", "").replace("на русском", "")
                fromLanguage, toLanguage = toLanguage, fromLanguage

            try:
                translation = Translator().translate(textToTranslate, dest=fromLanguage, src=toLanguage)
                return translation.text
            except:
                self.logger.log("Error: Check internet connection.")

        elif command == "weather":
            url = self.commandsData["urls"]["weather_api"]
            jsonData = getRequest(url).json()
            temperature = float(jsonData["main"]["temp"]) - 273.15 # from Kelvins to Celsius
            status = jsonData["weather"][0]["main"]

            if status == "Clear": # if if if if fififi if ifiififi fi ifif
                status = "Ясно"
            elif status == "Clouds":
                status = "Облачно"
            elif status == "Rain":
                status = "Дождь"

            # define word form
            temperature = round(temperature)
            wordForms = ["градус", "градуса", "градусов"]

            t = temperature

            if t >= 11 and t <= 19:
                degreesForm = wordForms[2]
   
            else:
                t %= 10
                if t == 1: degreesForm = wordForms[0]
                elif t >= 2 and t <= 4: degreesForm = wordForms[1]
                else: degreesForm = wordForms[2]

            return "{} {} по цельсию, {}".format(temperature, degreesForm, status)

        elif command == "wiki":
            recognizedText = remove_keywords(recognizedText, "wiki")

            try:
                text = erase_all_between_characters('(',')',Wikipedia.summary(recognizedText, sentences=2).replace('\u0301', ''))
                return text
            except:
                titles = Wikipedia.search(recognizedText)

                if len(titles) > 0:
                    page = erase_all_between_characters('(',')',Wikipedia.page(Wikipedia.search(titles[0])[0]))
                    return page.summary.split('\n')[:2]
                    
                else:
                    return "Извините, я не смогла найти информацию по вашему запросу."

        elif command == "when_happen":
            recognizedText = remove_keywords(recognizedText, "when_happen")

            queryParams = self.commandsData["data"]["wikipedia_search"]
            queryParams["search"] = recognizedText

            url = self.commandsData["urls"]["wikipedia"]["search"]
            request = getRequest(url, params=queryParams)

            try:
                eventUrl = self.commandsData["urls"]["wikipedia"]["."] + request.text.split("mw-search-result-heading")[1].split("</span>")[0].split("href=\"")[1].split("\"")[0]
                eventInfo = getRequest(eventUrl).text
                eventDate = eventInfo.split("<table class=\"infobox\"")[1].split("Дата")[1].split("</td>")[0]
                eventDate = erase_all_between_characters("<", ">", eventDate).replace("&#160;", " ")

                if "г" not in eventDate:
                    eventDate += " года"

                return eventDate.replace("г.", "года").replace("\n", "")

            except:
                return "Извините, я не смогла найти информацию по вашему запросу."

        elif command == "change_name":
            recognizedText = remove_keywords(recognizedText, "change_name")
            if recognizedText[0] == " ": recognizedText = recognizedText[1:]
            username = recognizedText.title()
            JsonData.get("Settings")["user"]["name"] = username
            JsonData.saveDataToFile("Settings")
            
            phrases = self.appData["phrases"]["change_name"]
            return "{} {}".format(self.chooseRandomPhrase(phrases), username)

        else:
            return "Команда не была распознана"
