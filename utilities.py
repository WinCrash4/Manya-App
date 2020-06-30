from classes.json_data_class import JsonData
from datetime import datetime


# Функции
def removeAlphaDigits(s):
    for word in s.split():
        if word.strip('.,').isdigit():
            yield word
        else:
            yield "".join(char for char in word if not char.isdigit())


def remove_keywords(text, command):
    for phrase in JsonData.get("AppData")["commands"][command]:
        text = text.replace(phrase, '')
        
    return text


def getElapsedTime(startTime):
    return datetime.now() - startTime


def erase_all_between_characters(start, end, text):
    out = ""
    flag = 0

    for i in text:
        if i == start:
            flag = 1
        elif i == end:
            flag = 0
        elif flag == 0:
            out += i

    return out

