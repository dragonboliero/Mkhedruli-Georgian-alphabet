'''
To do list:
            *Letters learning screen:
                - Record all sounds for Georgian letters.
            *Time attack screen:
                - Pass answer when pressing Enter/Return key.
            *Transcription screen:
                - Create a method which will change label with
                  correct answers (text language and score).
                - Create a method which will change background
                  of a letter the user needs to transcribe 
                  and make it move when the player provides 
                  input. Additionally, the function should
                  load a new line after inputting the last 
                  answer in the line. 
                - Create a label which will display % of correct
                  answers and maybe letters per minute statistics.
                - Fix the issue with punctuations not appearing
                  in the source text.
            *History of Georgian alphabets screen:
                - Collect data and write texts corresponding to
                  MDLabels.
            *Settings screen:
                - Option to change app background.
            *Achievements:
                - Create tiles, based on MDCards, for achievements 
                  in all modes. 
            *Other: 
                - Make it so that language name changes 
                  on all spinners.
                - Fix a bug which prevents sounds from being played
                  on Linux(probably also on Android). It's a known
                  Kivy issue. [Fixed with external library for now]
                - Male voice switch is activated whenever there is a 
                  click action anywhere in settings screen.
'''


from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager  import Screen,ScreenManager
from kivy.core.audio import SoundLoader
from kivy.uix.gridlayout import GridLayout
from kivy.uix.slider import Slider
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.core.window import Window
from kivy.clock import Clock
import data_loader as dl
import random
from playsound import playsound

load_strings = dl.load_lang_data()
load_settings = dl.load_settings()
transcription_texts = dl.load_transcription_texts()

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

'''
ModifiedSlider allows using on_release event instead of on_touch up
code created by hchandad
https://gist.github.com/hchandad/b71ed0e977e6d345bcb8
'''

class ScreenBackground(MDCard):
    pass

class ModifiedSlider(Slider):
    def __init__(self, **kwargs):
        self.register_event_type('on_release')
        super(ModifiedSlider, self).__init__(**kwargs)

    def on_release(self):
        pass

    def on_touch_up(self, touch):
        super(ModifiedSlider, self).on_touch_up(touch)
        if touch.grab_current == self:
            self.dispatch('on_release')
            return True

class TopPanel(GridLayout):
    pass

class SManager(ScreenManager):
    pass
class MainMenu(Screen):
    pass


#Main app
class Mkhedruli(MDApp):
    def build(self):    
        #Font with Georgian letters
        self.geo_font = '../geo_font.ttf'
        self.settings = load_settings
        self.current_lng = self.settings['language']
        self.language_strings = load_strings
        #Initial settings screen string
        self.settings_title = self.language_strings['settings'][self.settings['language']]
        #Initial screen background color
        self.screen_background_color = (0.3,0.5,0.7,1)
        #By default voice is set to male
        self.voice_switch_state = True
        #However if settings file says different the value needs to
        #changed
        if self.settings['voice'] == 'f':
            self.voice_switch_state = False
        #Value used in settings screen and Time Attack mode
        self.ta_minutes_value = int(int(self.settings['duration'])/60)
        #String used in settings screen for Time Attack duration label
        self.ta_default_duration = self.language_strings['ta_duration'][self.settings['language']] + str(self.ta_minutes_value)+':00'
        #String for letter tiles background in letter learing and Time Attack
        #modes.
        self.tile_bg_color = self.language_strings['tile_bg_color'][self.settings['language']]
        #String for screen background setting in settings screen
        self.screen_bg_color_string = self.language_strings['screen_bg_color'][self.settings['language']]
        #Total number of lines in all texts for transcription
        self.trans_lines_total = len(transcription_texts) - 1
        self.transcriptions = list(transcription_texts)
        #Counter for current transcription line
        self.tran_line = 1
        #Timer state in Time Attack mode
        self.counting_down = False
        #Time Attack clock object
        self.time_attack_clock = 0
        #Initial Time Attack correct answers string
        self.answer_streak_string_ta = self.language_strings['correct_answers_ta'][self.current_lng] + ' 0' 
        #Variable for storing whether it's the first quiz in Time Attack mode
        self.first_run_ta = False
        #Initial numer of correct answers in Time Attack mode
        self.answer_streak_score_ta = 0
        #Total number of answers in one run of Time Attack game
        self.all_answers_ta = 0
        #Time attack initial text
        self.time_attack_initial = self.language_strings['time_left'][self.settings['language']] + str(self.ta_minutes_value)+':00'
        #Read tiles background color from file and convert it from str to float
        color_values = self.settings['tile_bg_color_val'].split(',')
        float_color_values = [float(x) for x in color_values]
        self.default_card_color = tuple(float_color_values)
        #How much time does the player have in time attack mode for answers
        self.time_attack_seconds = int(self.settings['duration'])
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
        #Letters learning screen
        #Load app name in the new language
        self.root.get_screen('MainMenu').ids.apptitle.text = self.language_strings['app_name'][self.settings['language']]
        #If user changes language reload values of MDCards in the new language
        self.root.get_screen('MainMenu').ids.first_card_text.text = georgian_letters_dict[self.letters_pos[0][1]][self.settings['language']]
        self.root.get_screen('MainMenu').ids.second_card_text.text = georgian_letters_dict[self.letters_pos[1][1]][self.settings['language']]
        self.root.get_screen('MainMenu').ids.third_card_text.text = georgian_letters_dict[self.letters_pos[2][1]][self.settings['language']]
        self.root.get_screen('MainMenu').ids.fourth_card_text.text = georgian_letters_dict[self.letters_pos[3][1]][self.settings['language']]

        #Time Attack screen
        self.root.get_screen('MainMenu').ids.apptitle_ta.text = self.language_strings['app_name'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.timer.text = self.language_strings['time_left'][self.settings['language']] + str(self.time_attack_seconds)
        self.root.get_screen('MainMenu').ids.answer_streak_ta.text = self.language_strings['correct_answers_ta'][self.settings['language']] + ' ' + str(self.answer_streak_score_ta)

        #Transcription mode
        self.root.get_screen('MainMenu').ids.apptitle_trans.text=self.language_strings['app_name'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.streak_trans.text=self.answer_streak_string_ta = self.language_strings['correct_answers_ta'][self.settings['language']]+ '0'

        #History of Georgian alphabets
        self.root.get_screen('MainMenu').ids.apptitle_alph.text = self.language_strings['app_name'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.screen_title_alph.text = self.language_strings['title_alph'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.alph_general.label_text = self.language_strings['gen_alph'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.alph_asomtavruli.label_text = self.language_strings['asomtavruli'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.alph_nuskhuri.label_text = self.language_strings['nuskhuri'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.alph_mkhedruli.label_text = self.language_strings['mkhedruli'][self.settings['language']]

        #Settings screen
        self.root.get_screen('MainMenu').ids.settings_title.text = self.language_strings['settings'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.apptitle_settings.text = self.language_strings['app_name'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.voice_label.text = self.language_strings['voice'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.time_attack_duration_time.text = self.language_strings['ta_duration'][self.settings['language']] + str(self.ta_minutes_value)+ ':00'
        self.root.get_screen('MainMenu').ids.letter_tiles_bg_color.text = self.language_strings['tile_bg_color'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.screen_bg_color_set_label.text = self.language_strings['screen_bg_color'][self.settings['language']]

        #Achievements screen
        self.root.get_screen('MainMenu').ids.apptitle_achievements.text = self.language_strings['app_name'][self.settings['language']]

    #Function for picking random Georgian letter in letter learning mode
    def pick_georgian_letter(self,mode):
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
        #If letters learning mode
        if mode == 0:
            self.root.get_screen('MainMenu').ids.geo_letter.text = geo_letter_to_guess
        #If time attack mode
        if mode == 1:
            self.root.get_screen('MainMenu').ids.geo_letter_ta.text = geo_letter_to_guess

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
    def check_answer(self,geo_letter,answer,card_id,mode):
        
        #Letter learning mode
        if mode == 0:
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
        #Time Attack mode
        if mode == 1:
            #Add +1 to the counter no matter what is the answer
            self.all_answers_ta +=1
            if answer == georgian_letters_dict[geo_letter][self.settings['language']]:
                self.answer_streak_score_ta +=1
                self.root.get_screen('MainMenu').ids.answer_streak_ta.text = self.language_strings['correct_answers_ta'][self.current_lng] + ' ' + str(self.answer_streak_score_ta)
            self.root.get_screen('MainMenu').ids.TimeAttackAnswer.text=''


    #Method for playing letter sound in letter learning mode
    def play_letter_sound(self,letter_name):
        #For now, for testing purposes, there's only one sound 
        """ letter_sound = SoundLoader.load(f'data/audio/{letter_name}.mp3')
        if letter_sound:
            letter_sound.play() """
        voice_type = self.settings['voice']
        playsound(f'data/audio/{letter_name}{voice_type}.mp3')

    #Save settings to the file
    def save_settings(self):
        with open('data/settings.csv','w') as settings_file:
            for key,value in self.settings.items():
                settings_value = f'{key},{value}\n'
                settings_file.write(settings_value)  


    #Method starting timer in Time Attack mode
    def TimeAttackClock(self):
        #If it's used when countdown has not begin yet.
        if self.counting_down == False:
            self.time_attack_clock = Clock.schedule_interval(self.CallbackClock,1) 
            self.counting_down = True


    #Method returning value of time left in Time Attack mode
    def CallbackClock(self,dt):
        if self.time_attack_seconds > 0:
            self.time_attack_seconds -=1
            time_modulo = self.time_attack_seconds % 60
            minutes = str(int((self.time_attack_seconds - time_modulo) / 60))
            if time_modulo < 10:
                seconds = '0' + str(time_modulo)
            else:
                seconds = str(time_modulo)
            self.root.get_screen('MainMenu').ids.timer.text = self.language_strings['time_left'][self.settings['language']] + minutes + ':' + seconds
        else:
            self.counting_down = False
            self.time_attack_clock.cancel()
            self.time_attack_seconds = int(int(self.root.get_screen('MainMenu').ids.time_value.value) * 60)
            self.first_run_ta = True
            #Calculate % of correct answers in this run in Time Attack Mode
            percent_correct = (self.answer_streak_score_ta/self.all_answers_ta) * 100
            #Display statistics of this run in Time Attack mode
            display_run_stats = MDDialog(text=f"""
            {self.language_strings['time_up_ta'][self.settings['language']]}
            {self.language_strings['correct_answers_ta'][self.settings['language']]}{self.answer_streak_score_ta}
            {self.language_strings['perc_ca_ta'][self.settings['language']]}{percent_correct:.2f}
            """)
            display_run_stats.open()
            #Reset correct answers score and number of answers
            self.answer_streak_score_ta = 0
            self.all_answers_ta = 0
            self.root.get_screen('MainMenu').ids.answer_streak_ta.text = self.language_strings['correct_answers_ta'][self.current_lng] + ' ' + str(self.answer_streak_score_ta)  

    #Method swapping current MDLabel time value with slider value in Time Attack mode
    def ConvertTimeSliderValueToSeconds(self):
        if self.counting_down == False:
            self.root.get_screen('MainMenu').ids.timer.text = self.language_strings['time_left'][self.settings['language']] + str(int(self.root.get_screen('MainMenu').ids.time_value.value)) + ':00'
            self.time_attack_seconds = int(int(self.root.get_screen('MainMenu').ids.time_value.value) * 60)
    
    #Method displaying current line in transcription mode
    def GetTranscriptionLine(self):
            self.root.get_screen('MainMenu').ids.trans_text.text = transcription_texts[self.tran_line]
            if self.tran_line < self.trans_lines_total:
                self.tran_line +=1
            else:
                self.tran_line = 0

    #Method for displaying MDDialog with information about alphabets in Georgian alphabets'
    #history screen
    def history_screen_dialog(self,card_name,card_text):
        dialog_text = f"""
{self.language_strings[card_name][self.settings['language']]}

{self.language_strings[card_text][self.settings['language']]}
        """
        info_dialog = MDDialog(text=dialog_text,radius=[20,7,20,7])
        info_dialog.open()

    #Method for changing value of Time Attack duration in TA screen
    #settings screen and settings.csv file
    def change_time_attack_duration_values(self):
        self.ta_minutes_value = int(self.root.get_screen('MainMenu').ids.settings_time_value.value)
        #Change values in Time Attack mode screen
        #Initial timer value in Time Attack mode
        self.time_attack_seconds = self.ta_minutes_value * 60
        #Slider value
        self.root.get_screen('MainMenu').ids.time_value.value = self.ta_minutes_value
        #Label text
        self.root.get_screen('MainMenu').ids.timer.text = self.language_strings['time_left'][self.settings['language']] + str(int(self.root.get_screen('MainMenu').ids.time_value.value)) + ':00'
        #Change text displayed in settings menu
        self.ta_default_duration = self.language_strings['ta_duration'][self.settings['language']] + str(self.ta_minutes_value)+':00'
        self.root.get_screen('MainMenu').ids.time_attack_duration_time.text = self.ta_default_duration
        #Change value that will be saved in settings.csv file
        self.settings['duration'] = self.ta_minutes_value * 60

    #Change voice between male/female in settings menu
    def change_voice(self):
        if  self.voice_switch_state == True:
             self.voice_switch_state = False
             self.settings['voice'] = 'f'
        else:
             self.voice_switch_state = True
             self.settings['voice'] = 'm'

    #Makes tiles with color selection visible in settings screen
    def colors_visible(self):
        self.root.get_screen('MainMenu').ids.yellow.opacity = 1
        self.root.get_screen('MainMenu').ids.green.opacity = 1
        self.root.get_screen('MainMenu').ids.blue.opacity = 1
        self.root.get_screen('MainMenu').ids.red.opacity = 1

    #Method used after selecting tile background color in settings menu
    def select_color(self,color):
        #Makes tiles with color selection invisible in settings screen
        self.root.get_screen('MainMenu').ids.yellow.opacity = 0
        self.root.get_screen('MainMenu').ids.green.opacity = 0
        self.root.get_screen('MainMenu').ids.blue.opacity = 0
        self.root.get_screen('MainMenu').ids.red.opacity = 0
        #Change color of currently selected color in settings menu
        self.root.get_screen('MainMenu').ids.current_tile_bg_color.md_bg_color = color
        #Change value of variable with default tile background color
        self.default_card_color = color
        #Set new color value which will be saved to settings file
        self.settings['tile_bg_color_val'] = f"\"{color[0]},{color[1]},{color[2]},{color[3]}\""
        print(self.settings['tile_bg_color_val'])
        #Change color of tiles in all screens
        #Letters learning mode
        self.root.get_screen('MainMenu').ids.geo_letter_card.md_bg_color = color
        self.root.get_screen('MainMenu').ids.first_letter.md_bg_color = color
        self.root.get_screen('MainMenu').ids.second_letter.md_bg_color = color
        self.root.get_screen('MainMenu').ids.third_letter.md_bg_color = color
        self.root.get_screen('MainMenu').ids.fourth_letter.md_bg_color = color
        #Time Atack mode
        self.root.get_screen('MainMenu').ids.geo_letter_ta_card.md_bg_color = color
        #History of Georgian alphabets screen
        self.root.get_screen('MainMenu').ids.alph_general.md_bg_color = color
        self.root.get_screen('MainMenu').ids.alph_asomtavruli.md_bg_color = color
        self.root.get_screen('MainMenu').ids.alph_nuskhuri.md_bg_color = color
        self.root.get_screen('MainMenu').ids.alph_mkhedruli.md_bg_color = color

Mkhedruli().run()
