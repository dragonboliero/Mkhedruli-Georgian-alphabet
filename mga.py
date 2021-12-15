'''
To do list:
            *App design based on MDBottomNavigation
            *Main screen with letter learning mode
            *Time attack mode(?)
            *Screen with basic words learning.
            *Screen with history of Georgian writing.
            *Settings screen.
            *App strings in three languages: English, Polish and Russian
            *Achievements(?)
'''


from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager  import Screen,ScreenManager
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
import data_loader as dl
import random

load_strings = dl.load_lang_data()
load_settings = dl.load_settings()

georgian_letters_dict = {
'ა':{'en':'a','pl':'a','ru':'а'},'ბ':{'en':'b','pl':'b','ru':'б'},
'გ':{'en':'g','pl':'g','ru':'г'},'დ':{'en':'d','pl':'d','ru':'д'},
'ე':{'en':'e','pl':'e','ru':'э'},'ვ':{'en':'v','pl':'w','ru':'в'},
'ზ':{'en':'z','pl':'z','ru':'з'},'თ':{'en':'th','pl':'th','ru':'тх'},
'ი':{'en':'i','pl':'i','ru':'и'},'კ':{'en':'k\'','pl':'k\'','ru':'к\''},
'ლ':{'en':'l','pl':'l','ru':'л'},'მ':{'en':'m','pl':'m','ru':'м'},
'ნ':{'en':'n','pl':'n','ru':'н'},'ო':{'en':'o','pl':'o','ru':'о'},
'პ':{'en':'p\'','pl':'p\'','ru':'п\''},'ჟ':{'en':'zh','pl':'ż','ru':'ж'},
'რ':{'en':'r','pl':'r','ru':'р'},'ს':{'en':'s','pl':'s','ru':'с'},
'ტ':{'en':'t\'','pl':'t\'','ru':'т\''},'უ':{'en':'u','pl':'u','ru':'у'},
'ფ':{'en':'ph','pl':'ph','ru':'пх'},'ქ':{'en':'kh','pl':'kh','ru':'кх'},
'ღ':{'en':'gh','pl':'gh','ru':'гх'},'ყ':{'en':'q\'','pl':'q\'','ru':'к\''},
'შ':{'en':'sh','pl':'sz','ru':'ш'},'ჩ':{'en':'tshh','pl':'czh','ru':'чх'},
'ც':{'en':'tsh','pl':'tsh','ru':'цх'},'ძ':{'en':'dz','pl':'dz','ru':'дз'},
'წ':{'en':'ts\'','pl':'ts\'','ru':'ц\''},'ჭ':{'en':'tsh\'','pl':'cz\'','ru':'ч\''},
'ხ':{'en':'kh','pl':'kch','ru':'кх'},'ჯ':{'en':'j','pl':'dż','ru':'дж'},
'ჰ':{'en':'h','pl':'h','ru':'х'}
}

#Resolution which simulates mobile phone
Window.size = (405,900)

class SManager(ScreenManager):
    pass
class MainMenu(Screen):
    pass
class TopPanel(GridLayout):
    pass


#Main app
class Mkhedruli(MDApp):
    def build(self):    
        self.settings = load_settings
        self.language_strings = load_strings
        self.first_geo_letter = random.choice(list(georgian_letters_dict))
        self.first_correct_answer = georgian_letters_dict[self.first_geo_letter][self.settings['language']]
        self.first_random_letters = [random.choice(list(georgian_letters_dict.keys())) for letter in range(3)]
        self.first_random_letters = [georgian_letters_dict[self.first_random_letters[current_choice]][self.settings['language']] for current_choice in range(3)]
        app_uix = Builder.load_file('mga.kv')
        return app_uix

    #Function for changing language settings in the app
    def change_language(self, lang):
        self.settings['language'] = lang[-2:]
        self.root.get_screen('MainMenu').ids.apptitle.text = self.language_strings['app_name'][self.settings['language']]

    #Function for picking random Georgian letter in letter learning mode
    def pick_georgian_letter(self):
        self.root.get_screen('MainMenu').ids.geo_letter.text = random.choice(list(georgian_letters_dict))

Mkhedruli().run()