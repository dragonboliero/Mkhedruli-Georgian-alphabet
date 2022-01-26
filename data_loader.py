import csv
from inspect import _empty

def load_lang_data():
    strings = {}
    with open('data/strings.csv','r',encoding='utf8',newline='') as raw_lang_data:
            csv_data = csv.reader(raw_lang_data)
            for row in csv_data:
                property_name,en,pl,ru = row
                strings[property_name] = {'en':en,'pl':pl,'ru':ru}

    return strings

def load_settings():
    settings ={}
    with open('data/settings.csv','r') as raw_settings:
        csv_data = csv.reader(raw_settings)
        for row in csv_data:
            setting_name,value = row
            settings[setting_name] = value

    return settings


def load_transcription_texts():
    text = []
    with open('data/for_transcription.txt','r',encoding='utf-8') as text_file:
        for row in text_file:
            if row.strip() !='':
                text.append(row.strip())

    return text

def load_achievements():
    achievements = {}
    with open('data/achievements.csv','r') as raw_achievements:
        csv_data = csv.reader(raw_achievements)
        for row in csv_data:
            name,achievement_name_en,achievement_name_pl,achievement_name_ru,text_en,text_pl,text_ru = row
            achievements[name] = {'en':[achievement_name_en,text_en],'pl':[achievement_name_pl,text_pl],'ru':[achievement_name_ru,text_ru]}

    return achievements

def load_achievements_status():
    achievements_status = {}
    with open('data/achievement_status.csv','r') as raw_achievements_status:
        csv_data = csv.reader(raw_achievements_status)
        for row in csv_data:
            achievement_name,status,condition_counter = row
            achievements_status[achievement_name] = [status,condition_counter]

    return achievements_status
