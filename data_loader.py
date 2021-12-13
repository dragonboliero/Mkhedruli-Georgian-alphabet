import csv

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

data = load_settings()
print(data)
