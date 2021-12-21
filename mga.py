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
from kivy.clock import Clock
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
        self.current_lng = self.settings['language']
        self.language_strings = load_strings
        #Time attack initial text
        self.time_attack_initial = self.language_strings['time_left'][self.settings['language']] + '60'
        self.default_card_color = (0.2,0.1,1,1)
        #How much time does the player have in time attack mode for answers
        self.time_attack_seconds = 60
        #Copy of georgian_letters_dict that can be modified
        cp_georgian_letters_dict = dict(georgian_letters_dict)
        #Dictionary for storing user's language letters as keys and Georgian letters as values
        self.letters_dict ={}
        #Array for storing Georgian letters in given MDCard
        self.letters_pos = [[0],[1],[2],[3]]
        self.first_random_geo_letters =[]
        self.first_random_letters = []
        #Choose first Georgian letter
        self.first_geo_letter = random.choice(list(cp_georgian_letters_dict))
        #Pick  user's language equivalent
        self.first_correct_answer = cp_georgian_letters_dict[self.first_geo_letter][self.settings['language']]
        #Remove it from dictionary so that it's not repeated
        del cp_georgian_letters_dict[self.first_geo_letter]
        #Pick letters for another three MDCards and remove them from the copy of main dictionary
        for current_letter in range(3):
            self.first_random_geo_letters.append(random.choice(list(cp_georgian_letters_dict.keys())))    
            self.first_random_letters.append(cp_georgian_letters_dict[self.first_random_geo_letters[current_letter]][self.settings['language']])
            del cp_georgian_letters_dict[self.first_random_geo_letters[current_letter]]    
        #Add correct answer to three wrong answers
        self.first_random_letters.append(self.first_correct_answer)

        #Create a backward dictionary where user's equivalent is a key
        for letter in range(3):
            self.letters_dict[self.first_random_letters[letter]] = self.first_random_geo_letters[letter]
        self.letters_dict[self.first_correct_answer] = self.first_geo_letter

        #Set random positions to all letters
        self.shuffled_first_letters = random.sample(self.first_random_letters,len(self.first_random_letters))

        #Assign Georgian letters to their position on MDCards
        for geo_letter in range(4):
            self.letters_pos[geo_letter].append(self.letters_dict[self.shuffled_first_letters[geo_letter]])
        
        app_uix = Builder.load_file('mga.kv')
        return app_uix


    #Function for changing language settings in the app
    def change_language(self, lang):
        self.settings['language'] = lang[-2:]
        #Load app name in the new language
        self.root.get_screen('MainMenu').ids.apptitle.text = self.language_strings['app_name'][self.settings['language']]
        #If user changes language reload values of MDCards in the new language
        self.root.get_screen('MainMenu').ids.first_card_text.text = georgian_letters_dict[self.letters_pos[0][1]][self.settings['language']]
        self.root.get_screen('MainMenu').ids.second_card_text.text = georgian_letters_dict[self.letters_pos[1][1]][self.settings['language']]
        self.root.get_screen('MainMenu').ids.third_card_text.text = georgian_letters_dict[self.letters_pos[2][1]][self.settings['language']]
        self.root.get_screen('MainMenu').ids.fourth_card_text.text = georgian_letters_dict[self.letters_pos[3][1]][self.settings['language']]
        self.root.get_screen('MainMenu').ids.timer.text = self.language_strings['time_left'][self.settings['language']] + str(self.time_attack_seconds)


    #Function for picking random Georgian letter in letter learning mode
    def pick_georgian_letter(self):
        #Copy of georgian_letters_dict that can be modified
        cp_georgian_letters_dict = dict(georgian_letters_dict)
        new_random_geo_letters = []
        new_random_letters = []
        #Dictionary for storing user's language letters as keys and Georgian letters as values
        letters_pair = {}
        #Array for storing Georgian letters in given MDCard
        new_letters_pos = [[0],[1],[2],[3]]
        #Get random Georgian letter to guess and assign it to MDCard
        geo_letter_to_guess = random.choice(list(cp_georgian_letters_dict))
        self.root.get_screen('MainMenu').ids.geo_letter.text = geo_letter_to_guess
        #Associate Georgian letter with user native lng letter and delete it from the main dictionary
        new_correct_letter = cp_georgian_letters_dict[geo_letter_to_guess][self.settings['language']]
        del cp_georgian_letters_dict[geo_letter_to_guess]
        #Choose three random letters for other MDCards and remove them from the main dictionary
        for current_letter in range(3):
            new_random_geo_letters.append(random.choice(list(cp_georgian_letters_dict.keys())))
            new_random_letters.append(cp_georgian_letters_dict[new_random_geo_letters[current_letter]][self.settings['language']])
            #Associate user's language letter with Georgian letter
            letters_pair[new_random_letters[current_letter]] = new_random_geo_letters[current_letter]
            del cp_georgian_letters_dict[new_random_geo_letters[current_letter]]
        #Add correct answer to the same array as wrong answers
        new_random_letters.append(new_correct_letter)
        #Add correct answer pair
        letters_pair[new_correct_letter] = geo_letter_to_guess
        
        #Pick random letter from the array and then associate it with all MDCards and it's position
        random_to_add = random.choice(new_random_letters)
        new_letters_pos[0].append(letters_pair[random_to_add])
        self.root.get_screen('MainMenu').ids.first_card_text.text = random_to_add
        self.root.get_screen('MainMenu').ids.first_letter.md_bg_color = self.default_card_color
        new_random_letters.remove(random_to_add)

        random_to_add = random.choice(new_random_letters)
        new_letters_pos[1].append(letters_pair[random_to_add])
        self.root.get_screen('MainMenu').ids.second_card_text.text = random_to_add
        self.root.get_screen('MainMenu').ids.second_letter.md_bg_color = self.default_card_color
        new_random_letters.remove(random_to_add)

        random_to_add = random.choice(new_random_letters)
        new_letters_pos[2].append(letters_pair[random_to_add])
        self.root.get_screen('MainMenu').ids.third_card_text.text = random_to_add
        self.root.get_screen('MainMenu').ids.third_letter.md_bg_color = self.default_card_color
        new_random_letters.remove(random_to_add)

        random_to_add = random.choice(new_random_letters)
        new_letters_pos[3].append(letters_pair[random_to_add])
        self.root.get_screen('MainMenu').ids.fourth_card_text.text = random_to_add
        self.root.get_screen('MainMenu').ids.fourth_letter.md_bg_color = self.default_card_color
        new_random_letters.remove(random_to_add)
        
        #Return positions of picked values needed to be used when chaning language
        self.letters_pos = new_letters_pos


    #Checks if user answer is correct
    def check_answer(self,geo_letter,answer,card_id):

        if answer == georgian_letters_dict[geo_letter][self.settings['language']]:
            if card_id == 0:
                self.root.get_screen('MainMenu').ids.first_letter.md_bg_color = (0,1,0,1)
            if card_id == 1:
                self.root.get_screen('MainMenu').ids.second_letter.md_bg_color = (0,1,0,1)
            if card_id == 2:
                self.root.get_screen('MainMenu').ids.third_letter.md_bg_color = (0,1,0,1)
            if card_id == 3:
                self.root.get_screen('MainMenu').ids.fourth_letter.md_bg_color = (0,1,0,1)
        else:
            if card_id == 0:
                self.root.get_screen('MainMenu').ids.first_letter.md_bg_color = (1,0,0,1)
            if card_id == 1:
                self.root.get_screen('MainMenu').ids.second_letter.md_bg_color = (1,0,0,1)
            if card_id == 2:
                self.root.get_screen('MainMenu').ids.third_letter.md_bg_color = (1,0,0,1)
            if card_id == 3:
                self.root.get_screen('MainMenu').ids.fourth_letter.md_bg_color = (1,0,0,1)


    #Save settings to the file
    def save_settings(self,screen):
        with open('data/settings.csv','w') as settings_file:
            for key,value in self.settings.items():
                settings_value = f'{key},{value}\n'
                settings_file.write(settings_value)  


    #Method starting timer in Time Attack mode
    def TimeAttackClock(self):
        Clock.schedule_interval(self.CallbackClock,1)      


    #Method returning value of time left in Time Attack mode
    def CallbackClock(self,dt):
        if self.time_attack_seconds > 1:
            self.time_attack_seconds -=1
            time_modulo = self.time_attack_seconds % 60
            minutes = str(int((self.time_attack_seconds - time_modulo) / 60))
            if time_modulo < 10:
                seconds = '0' + str(time_modulo)
            else:
                seconds = str(time_modulo)
            self.root.get_screen('MainMenu').ids.timer.text = self.language_strings['time_left'][self.settings['language']] + minutes + ':' + seconds


    #Method swapping current MDLabel time value with slider value in Time Attack mode
    def ConvertTimeSliderValueToSeconds(self):
        self.root.get_screen('MainMenu').ids.timer.text = self.language_strings['time_left'][self.settings['language']] + str(int(self.root.get_screen('MainMenu').ids.time_value.value)) + ':00'
        self.time_attack_seconds = int(int(self.root.get_screen('MainMenu').ids.time_value.value) * 60)


Mkhedruli().run()
