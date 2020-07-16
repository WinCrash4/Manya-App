# Импортируем классы
from utilities import *

from datetime import datetime, timedelta
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

        self.loopEnable = True

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

            return {"pronounce": greetings, "display": greetings}

        elif command == "ctime":
            time = datetime.now()
            time = "Сейчас " + str(time.hour) + ":" + str(time.minute) + ":" + str(time.second) 
            return {"pronounce": time, "display": time}

        elif command == "all_commands_info":
            pronounce = self.chooseRandomPhrase(self.appData["phrases"]["all_commands_info"]) + '\n'
            display = pronounce

            for _, infoAndPhrases in JsonData.get("AppData")["commands"].items():
                if infoAndPhrases[0] != "hidden":
                    display += "{} - {}\n".format(infoAndPhrases[0], ", ".join(Random.sample(infoAndPhrases[1], 2)))
            return {"pronounce": pronounce, "display": display}

        elif command == "music":
            musicIndex = 0
            matchingNamesCount = 0
            matchingWordsCount = 0
            musicDirectory = str(JsonData.get("Settings")["user"]["music_folder"])

            if musicDirectory == "":
                res = "Папка с музыкой не назначена"
                return {"pronounce": res, "display": res, "music_name": None}

            recognizedText = remove_keywords(recognizedText, "music")
            
            if len(recognizedText) != 0: # for case if user didn't told the name of the music
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
                    res = "Я не нашла музыку с таким названием"
                    musicName = None

                elif matchingNamesCount == 1:
                    #OS.startfile(musicDirectory + OS.listdir(path = musicDirectory)[musicIndex])
                    res = "Включаю музыку"
                    musicName = str(OS.listdir(path = musicDirectory)[musicIndex])

                elif matchingNamesCount > 1:
                    res = "Здесь слишком много песен с таким названием, уточните свой запрос"
                    musicName = None

                matchingNamesCount = 0

            else:
                musicIndex = Random.randint(0,len(OS.listdir(path = musicDirectory)))
                while OS.listdir(path = musicDirectory)[musicIndex][-4:] != ".mp3":
                    musicIndex = Random.randint(0,len(OS.listdir(path = musicDirectory)))
                res = "Включаю музыку"
                musicName = str(OS.listdir(path = musicDirectory)[musicIndex])
                #OS.startfile(musicDirectory + OS.listdir(path = musicDirectory)[musicIndex])

            return {"pronounce": res, "display": res, "music_name": musicName}

        elif command == "music_disable":
            for pid in (process.pid for process in PSUtil.process_iter() if process.name() == "AIMP.exe"):
                OS.system("taskkill /im  AIMP.exe") # AIMP - name of music player
            self.pronounce("Музыка выключена")

        elif command == "joke":
            jokes = jsonLoad(file.read())["jokes"] 
            joke = self.chooseRandomPhrase(jokes)
            return {"pronounce": joke, "display": joke}

        elif command == "thanks":
            thanks = self.appData["phrases"]["thanks"] 
            res = self.chooseRandomPhrase(thanks)
            return {"pronounce": res, "display": res}

        elif command == "compliment":
            compliments = self.appData["phrases"]["compliment"] 
            compliment = self.chooseRandomPhrase(compliments)
            return {"pronounce": compliment, "display": compliment}

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
                return {"pronounce": translation.text, "display": translation.text}
            except:
                return {"pronounce": "Ошибка интернет-соединения", "display": "Ошибка интернет-соединения"}    

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

            res = "{} {} по цельсию, {}".format(temperature, degreesForm, status)

            return {"pronounce": res, "display": res} 

        elif command == "wiki":
            recognizedText = remove_keywords(recognizedText, "wiki")
            if recognizedText == "":
                res = "Пожалуйста, повторите ваш запрос"
                return {"pronounce": res, "display": res}

            try:
                text = erase_all_between_characters('(',')',Wikipedia.summary(recognizedText, sentences=3).replace('\u0301', ''))
                return {"pronounce": text, "display": text}
            except:
                titles = Wikipedia.search(recognizedText)

                if len(titles) > 0:
                    page = erase_all_between_characters('(',')',Wikipedia.page(Wikipedia.search(titles[0])[0]))
                    return {"pronounce": page.summary.split('\n')[:2], "display": page.summary.split('\n')[:2]}
                    
                else:
                    res = "Извините, я не смогла найти информацию по вашему запросу."
                    return {"pronounce": res, "display": res}

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

                res = eventDate.replace("г.", "года").replace("\n", "")
                return {"pronounce": res, "display": res}

            except:
                res = "Извините, я не смогла найти информацию по вашему запросу."
                return {"pronounce": res, "display": res}

        elif command == "change_name":
            recognizedText = remove_keywords(recognizedText, "change_name")
            if recognizedText[0] == " ": recognizedText = recognizedText[1:]
            username = recognizedText.title()
            JsonData.get("Settings")["user"]["name"] = username
            JsonData.saveDataToFile("Settings")
            
            phrases = self.appData["phrases"]["change_name"]
            res = "{} {}".format(self.chooseRandomPhrase(phrases), username)
            return {"pronounce": res, "display": res}

        else:
            res = "Команда не была распознана"
            return {"pronounce": res, "display": res}
