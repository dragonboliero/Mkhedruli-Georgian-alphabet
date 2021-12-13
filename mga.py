from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager  import Screen,ScreenManager
import data_loader as dl

load_strings = dl.load_lang_data()
load_settings = dl.load_settings()

class SManager(ScreenManager):
    pass
class MainMenu(Screen):
    pass


class Mkhedruli(MDApp):


    def build(self):    
        self.settings = load_settings
        self.language_strings = load_strings
        app_uix = Builder.load_file('mga.kv')
        return app_uix

    def change_language(self, lang):
        self.settings['language'] = lang[-2:]
        self.root.get_screen('MainMenu').ids.apptitle.text = ''
        self.root.get_screen('MainMenu').ids.apptitle.text = self.language_strings['app_name'][self.settings['language']]
        print(self.root.get_screen('MainMenu').ids.apptitle.text)

Mkhedruli().run()