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
georgian_letters = ['ა','ბ','გ','დ','ე','ვ','ზ','თ','ი','კ','ლ','მ','ნ','ო',
'პ','ჟ','რ','ს','ტ','უ','ფ','ქ','ღ','ყ','შ','ჩ','ც','ძ','წ','ჭ','ხ','ჯ','ჰ']

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
        app_uix = Builder.load_file('mga.kv')
        return app_uix

    #Function for changing language settings in the app
    def change_language(self, lang):
        self.settings['language'] = lang[-2:]
        self.root.get_screen('MainMenu').ids.apptitle.text = self.language_strings['app_name'][self.settings['language']]

    #Function for picking random Georgian letter in letter learning mode
    def pick_georgian_letter(self):
        self.root.get_screen('MainMenu').ids.geo_letter.text = random.choice(georgian_letters)

Mkhedruli().run()