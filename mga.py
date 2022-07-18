'''
playsound 1.2.2 library is required to work on Windows. The latest 
version - 1.3 - doesn't play sound.
To do list:
            *Letters learning screen:
                - Record all sounds for Georgian letters.
                - Better format alphabet chart MDDialog.
            *Time attack screen:
            *Transcription screen:
                - Find a way to show to the user that space is 
                  currently selected.
                - Fix the issue with punctuations not appearing
                  in the source text.
            *History of Georgian alphabets screen:
                - Collect data and write texts corresponding to
                  MDLabels.
            *Other: 
                - Make it so that language name changes 
                  on all spinners.
                - Fix a bug which prevents sounds from being played
                  on Linux(probably also on Android). It's a known
                  Kivy issue. [Fixed with external library for now]
                - Male voice switch is activated whenever there is a 
                  click action anywhere in settings screen.
'''


from logging import root
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
import locale

load_strings = dl.load_lang_data()
load_settings = dl.load_settings()
transcription_texts = dl.load_transcription_texts()
achievement_texts = dl.load_achievements()
achievement_status = dl.load_achievements_status()


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


#Modified KivyMD elements
class ScreenBackground(MDCard):
    pass

'''
ModifiedSlider allows using on_release event instead of on_touch up
code created by hchandad
https://gist.github.com/hchandad/b71ed0e977e6d345bcb8
'''
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

#KivyMD screens
class SManager(ScreenManager):
    pass
class MainMenu(Screen):
    pass

#Main app
class Mkhedruli(MDApp):
    def build(self):  
        print(locale.getlocale())
        #Font with Georgian letters
        self.geo_font = '../geo_font.ttf'
        #Variable holding app settings
        self.settings = load_settings
        #Variable holding strings used in the app
        self.language_strings = load_strings
        #Variable holding currently selected language //Used for initialization in kv file
        self.current_lng = self.settings['language']
        #Variable holding dictionary with achievements texts
        self.achievement_strings = achievement_texts
        #Variable holding status of achievements
        self.achievements_status = achievement_status
        #Variable storing type of background color to change in settings screen
        self.bg_color_type = 'tile'
        #Initial settings screen string
        self.settings_title = self.language_strings['settings'][self.settings['language']]
        #By default voice is set to male
        self.voice_switch_state = True
        #However if settings file says different the value needs to
        #changed
        if self.settings['voice'] == 'f':
            self.voice_switch_state = False
        #Value used in settings screen and Time Attack mode for displaying duration time in minutes
        self.ta_minutes_value = int(int(self.settings['duration'])/60)
        #String used in settings screen for Time Attack duration label
        self.ta_default_duration = self.language_strings['ta_duration'][self.settings['language']] + '\n'+ str(self.ta_minutes_value)+':00'
        #String for tiles background setting in settings screen.
        self.tile_bg_color = self.language_strings['tile_bg_color'][self.settings['language']]
        #String for screen background setting in settings screen
        self.screen_bg_color_string = self.language_strings['screen_bg_color'][self.settings['language']]
        #Initial position in transcription string
        self.trans_pos_counter = 1
        #Total number of lines of transcription text
        self.trans_lines_total = len(transcription_texts) - 1
        #Current line number in transcribed text
        self.trans_current_line_number = 0 
        #Transcription text converted to separate lines
        self.transcriptions = list(transcription_texts)
        #Current line displayed in Transcription mode with current letter highlighted 
        self.current_transcription_line = f"[color=fcba03]{self.transcriptions[0][0]}[/color]{self.transcriptions[0][1:]}"
        #Current letter to transcribe in transcription mode
        self.trans_current_letter = self.transcriptions[0][0]
        #Score counter for transcription mode
        self.trans_score = 0
        #Total number of user answers in Transcription mode duiring current session
        self.trans_answers = 0
        #Correct answers percentage in Transcription mode during current session
        self.trans_percentage = 0
        #String for percentage of correct answers in transcription mode
        self.trans_percentage_string = self.language_strings['perc_ca_ta'][self.settings['language']] + str(self.trans_percentage)
        #Letter position in current line / for answer checking purposes
        self.trans_index = 0
        #Current line number / for answer checking purposes
        self.trans_check_line = 0
        #Timer state in Time Attack mode
        self.counting_down = False
        #Time Attack clock object
        self.time_attack_clock = 0
        #Initial Time Attack correct answers string
        self.answer_streak_string_ta = self.language_strings['correct_answers_ta'][self.settings['language']] + '\n' + ' 0' 
        #Variable for storing whether it's the first quiz in Time Attack mode
        self.first_run_ta = False
        #Initial numer of correct answers in Time Attack mode
        self.answer_streak_score_ta = 0
        #Total number of answers in one run of Time Attack game
        self.all_answers_ta = 0
        #Time attack initial text
        self.ta_init_txt = self.language_strings['time_left'][self.settings['language']].split(" ")
        self.time_attack_initial = self.ta_init_txt[0] + " " + self.ta_init_txt[1] + "\n" + str(self.ta_minutes_value)+':00'
        #Read screen background color from file and convert it from str to float
        screen_bg_color_values = self.settings['screen_bg_color_val'].split(',')
        float_screen_bg_color_values = [float(x) for x in screen_bg_color_values]
        self.screen_background_color = tuple(float_screen_bg_color_values)
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
        
        #Variable holding number of learned letters        
        self.number_learned_letters = int(self.achievements_status['achievement_letters'][0])
        #Variable holding all learned letters
        self.learned_letters = self.achievements_status['achievement_letters'][1]
        #Change status of Letter Learning mode achievement tiles in Achievements screen
        self.achievement_ll1_notclickable = True
        if int(self.achievements_status['achievement_letters'][0]) >= 10:
            self.achievement_ll1_notclickable = False
        self.achievement_ll2_notclickable = True
        if int(self.achievements_status['achievement_letters'][0]) >= 20:
            self.achievement_ll2_notclickable = False
        self.achievement_ll3_notclickable = True
        if int(self.achievements_status['achievement_letters'][0]) == 33:
            self.achievement_ll3_notclickable = False

        #Change status of Time Attack mode achievement tiles in Achievement screen
        self.achievement_ta1_notclickable = True
        if int(self.achievements_status['achievement_time_attack'][0]) >= 1:
            self.achievement_ta1_notclickable = False
        self.achievement_ta2_notclickable = True
        if int(self.achievements_status['achievement_time_attack'][0]) >= 2:
            self.achievement_ta2_notclickable = False
        self.achievement_ta3_notclickable = True
        if int(self.achievements_status['achievement_time_attack'][0]) >= 3:
            self.achievement_ta3_notclickable = False

        #Setting up 'clickability' of achievement tiles in Achievement screen
        self.achievement_history_notclickable = True
        if self.achievements_status['achievement_history'][0] == '1':
            self.achievement_history_notclickable = False

        app_uix = Builder.load_file('mga.kv')
        return app_uix

    #Method displaying letters of Georgian alphabet with corresponding user's native language equivalents
    def display_alphabet_chart(self,font_size):
        f_size = int(font_size)
        chart_text=f'''[size={f_size}][b]
[font=data/geo_font.ttf]ა[/font] - {georgian_letters_dict['ა'][self.settings['language']]}    [font=data/geo_font.ttf]ბ[/font] - {georgian_letters_dict['ბ'][self.settings['language']]}        [font=data/geo_font.ttf]  გ [/font] - {georgian_letters_dict['გ'][self.settings['language']]}
[font=data/geo_font.ttf]დ[/font] - {georgian_letters_dict['დ'][self.settings['language']]}    [font=data/geo_font.ttf]ე[/font] - {georgian_letters_dict['ე'][self.settings['language']]}        [font=data/geo_font.ttf]  ვ [/font] - {georgian_letters_dict['ვ'][self.settings['language']]}
[font=data/geo_font.ttf]ზ[/font] - {georgian_letters_dict['ზ'][self.settings['language']]}    [font=data/geo_font.ttf]  თ [/font] - {georgian_letters_dict['თ'][self.settings['language']]}     [font=data/geo_font.ttf]  ი [/font] - {georgian_letters_dict['ი'][self.settings['language']]}
[font=data/geo_font.ttf]კ[/font] - {georgian_letters_dict['კ'][self.settings['language']]}    [font=data/geo_font.ttf]  ლ [/font] - {georgian_letters_dict['ლ'][self.settings['language']]}     [font=data/geo_font.ttf]  მ [/font] - {georgian_letters_dict['მ'][self.settings['language']]}
[font=data/geo_font.ttf]ნ[/font] - {georgian_letters_dict['ნ'][self.settings['language']]}    [font=data/geo_font.ttf]  ო [/font] - {georgian_letters_dict['ო'][self.settings['language']]}     [font=data/geo_font.ttf]  პ [/font] - {georgian_letters_dict['პ'][self.settings['language']]}
[font=data/geo_font.ttf]ჟ[/font] - {georgian_letters_dict['ჟ'][self.settings['language']]}    [font=data/geo_font.ttf]  რ [/font] - {georgian_letters_dict['რ'][self.settings['language']]}     [font=data/geo_font.ttf]  ს [/font] - {georgian_letters_dict['ს'][self.settings['language']]}
[font=data/geo_font.ttf]ტ[/font] - {georgian_letters_dict['ტ'][self.settings['language']]}    [font=data/geo_font.ttf]  უ [/font] - {georgian_letters_dict['უ'][self.settings['language']]}     [font=data/geo_font.ttf]  ფ [/font] - {georgian_letters_dict['ფ'][self.settings['language']]}
[font=data/geo_font.ttf]ქ[/font] - {georgian_letters_dict['ქ'][self.settings['language']]}    [font=data/geo_font.ttf]  ღ [/font] - {georgian_letters_dict['ღ'][self.settings['language']]}     [font=data/geo_font.ttf]  ყ [/font] - {georgian_letters_dict['ყ'][self.settings['language']]}
[font=data/geo_font.ttf]შ[/font] - {georgian_letters_dict['შ'][self.settings['language']]}    [font=data/geo_font.ttf]  ჩ [/font] - {georgian_letters_dict['ჩ'][self.settings['language']]}     [font=data/geo_font.ttf]  ც [/font] - {georgian_letters_dict['ც'][self.settings['language']]}
[font=data/geo_font.ttf]ძ[/font] - {georgian_letters_dict['ძ'][self.settings['language']]}    [font=data/geo_font.ttf]  წ [/font] - {georgian_letters_dict['წ'][self.settings['language']]}     [font=data/geo_font.ttf]  ჭ [/font] - {georgian_letters_dict['ჭ'][self.settings['language']]}
[font=data/geo_font.ttf]ხ[/font] - {georgian_letters_dict['ხ'][self.settings['language']]}    [font=data/geo_font.ttf]  ჯ [/font] - {georgian_letters_dict['ჯ'][self.settings['language']]}     [font=data/geo_font.ttf]  ჰ [/font] - {georgian_letters_dict['ჰ'][self.settings['language']]}[/b][/size]'''
        chart_dialog = MDDialog(title=self.language_strings['app_name'][self.settings['language']],text=chart_text)
        chart_dialog.open()

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
        self.ta_init_txt = self.language_strings['time_left'][self.settings['language']].split(" ")
        self.root.get_screen('MainMenu').ids.timer.text = self.ta_init_txt[0] + " " + self.ta_init_txt[1] + "\n" + str(int(self.root.get_screen('MainMenu').ids.time_value.value)) + ":00"
        self.root.get_screen('MainMenu').ids.answer_streak_ta.text = self.language_strings['correct_answers_ta'][self.settings['language']] + ' ' + str(self.answer_streak_score_ta)

        #Transcription mode
        self.root.get_screen('MainMenu').ids.apptitle_trans.text=self.language_strings['app_name'][self.settings['language']]
        self.root.get_screen('MainMenu').ids.streak_trans.text=self.answer_streak_string_ta = self.language_strings['correct_answers_ta'][self.settings['language']]+ '\n' + str(self.trans_score)
        self.root.get_screen('MainMenu').ids.percentage_trans.text=self.language_strings['perc_ca_ta'][self.settings['language']] + str(self.trans_percentage)

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
        self.root.get_screen('MainMenu').ids.achievement_ll1.label_text = self.achievement_strings['achievement_ll1'][self.settings['language']][0]
        self.root.get_screen('MainMenu').ids.achievement_ll2.label_text = self.achievement_strings['achievement_ll2'][self.settings['language']][0]
        self.root.get_screen('MainMenu').ids.achievement_ll3.label_text = self.achievement_strings['achievement_ll3'][self.settings['language']][0]
        self.root.get_screen('MainMenu').ids.achievement_ta1.label_text = self.achievement_strings['achievement_ta1'][self.settings['language']][0]
        self.root.get_screen('MainMenu').ids.achievement_ta2.label_text = self.achievement_strings['achievement_ta2'][self.settings['language']][0]
        self.root.get_screen('MainMenu').ids.achievement_ta3.label_text = self.achievement_strings['achievement_ta3'][self.settings['language']][0]
        self.root.get_screen('MainMenu').ids.achievement_trans1.label_text = self.achievement_strings['achievement_trans1'][self.settings['language']][0]
        self.root.get_screen('MainMenu').ids.achievement_trans2.label_text = self.achievement_strings['achievement_trans2'][self.settings['language']][0]
        self.root.get_screen('MainMenu').ids.achievement_trans3.label_text = self.achievement_strings['achievement_trans3'][self.settings['language']][0]
        self.root.get_screen('MainMenu').ids.achievement_history.label_text = self.achievement_strings['achievement_history'][self.settings['language']][0]

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
                self.check_achievement_letters(geo_letter)
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
                self.root.get_screen('MainMenu').ids.answer_streak_ta.text = self.language_strings['correct_answers_ta'][self.settings['language']] + ' ' + str(self.answer_streak_score_ta)
            self.root.get_screen('MainMenu').ids.TimeAttackAnswer.text=''

        #Transcription mode
        if mode == 2:
            #Check if currently selected sign is a Georgian letter
            if self.trans_current_letter in georgian_letters_dict:
                #If it is check if user input was correct and if so add point
                if answer == georgian_letters_dict[self.trans_current_letter][self.settings['language']]:
                    self.trans_score += 1
                    self.root.get_screen('MainMenu').ids.streak_trans.text = self.language_strings['correct_answers_ta'][self.settings['language']] + str(self.trans_score)
                #Increment answers counter
                self.trans_answers +=1
            #Move to next letter if it's not the end of the current line 
            if self.trans_index < len(self.transcriptions[self.trans_check_line]):
                self.trans_index +=1
            #If it is, reset index position to 0
            if self.trans_index == len(self.transcriptions[self.trans_check_line]):
                self.trans_index = 0
                #And increment line number
                if self.trans_check_line < len(self.transcriptions):
                    self.trans_check_line +=1 
                #Or go to the beginning if it was a last line
                if self.trans_check_line == len(self.transcriptions):
                    self.trans_check_line = 0
            self.trans_current_letter  = self.transcriptions[self.trans_check_line][self.trans_index]
            #Calculate percentage of correct answers and update label
            self.trans_percentage = int((self.trans_score / self.trans_answers) * 100)
            self.root.get_screen('MainMenu').ids.percentage_trans.text = self.language_strings['perc_ca_ta'][self.settings['language']] + str(self.trans_percentage)
                


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
                if key == 'tile_bg_color_val' or 'screen_bg_color_val':
                    settings_value = f'{key},\"{value}\"\n'
                else:
                    settings_value = f'{key},{value}\n'
                settings_file.write(settings_value)  

    #resets all values upon entering TimeAttack mode
    def Reset_TimeAttack(self):
        try:
            self.time_attack_clock.cancel()
        except:
            print('Clock not running')
        minutes = str(int(int(self.settings['duration']) / 60))
        self.root.get_screen('MainMenu').ids.timer.text =  self.ta_init_txt[0] + " " + self.ta_init_txt[1] + "\n" + minutes + ':00'
        self.root.get_screen('MainMenu').ids.answer_streak_ta.text = self.language_strings['correct_answers_ta'][self.settings['language']] + '0'
        self.pick_georgian_letter(1)



    #Method starting timer in Time Attack mode
    def TimeAttackClock(self):
        #If it's used when countdown has not begin yet.
        if self.counting_down == False:
            self.time_attack_clock = Clock.schedule_interval(self.CallbackClock,1) 
            self.counting_down = True


    #Method returning value of time left in Time Attack mode
    def CallbackClock(self,dt):
        if self.time_attack_seconds > 0:
            self.root.get_screen('MainMenu').ids.time_value.disabled = True
            self.time_attack_seconds -=1
            time_modulo = self.time_attack_seconds % 60
            minutes = str(int((self.time_attack_seconds - time_modulo) / 60))
            if time_modulo < 10:
                seconds = '0' + str(time_modulo)
            else:
                seconds = str(time_modulo)
            timer_text = self.language_strings['time_left'][self.settings['language']].split(" ")
            self.root.get_screen('MainMenu').ids.timer.text = timer_text[0] + " " + timer_text[1] + "\n" + minutes + ':' + seconds
        else:
            self.root.get_screen('MainMenu').ids.time_value.disabled = False
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
            self.check_achievement_ta()
            #Reset correct answers score and number of answers
            self.answer_streak_score_ta = 0
            self.all_answers_ta = 0
            self.root.get_screen('MainMenu').ids.answer_streak_ta.text = self.language_strings['correct_answers_ta'][self.settings['language']] + ' ' + str(self.answer_streak_score_ta)  

    #Method swapping current MDLabel time value with slider value in Time Attack mode
    def ConvertTimeSliderValueToSeconds(self):
        if self.counting_down == False:
            self.root.get_screen('MainMenu').ids.timer.text = self.ta_init_txt[0] + " " + self.ta_init_txt[1] + "\n" + str(int(self.root.get_screen('MainMenu').ids.time_value.value)) + ':00'
            self.time_attack_seconds = int(int(self.root.get_screen('MainMenu').ids.time_value.value) * 60)

    #Method for resetting values in Transcription mode
    def Reset_Transcription(self):
        #Reset variables
        self.trans_index = 0
        self.trans_check_line = 0
        self.trans_pos_counter = 1
        self.trans_current_line_number = 0
        self.trans_score = 0
        self.trans_current_letter = self.transcriptions[0][0]
        self.trans_percentage = 0
        self.trans_answers = 0
        #Update strings in Transcription screen
        self.root.get_screen('MainMenu').ids.streak_trans.text = self.language_strings['correct_answers_ta'][self.settings['language']] + str(self.trans_score)
        self.root.get_screen('MainMenu').ids.trans_text.text = f"[color=fcba03]{self.transcriptions[0][0]}[/color]{self.transcriptions[0][1:]}"
        self.root.get_screen('MainMenu').ids.percentage_trans.text = self.language_strings['perc_ca_ta'][self.settings['language']] + str(self.trans_percentage)

    #Method moving highlighted letter in transcription mode
    def HighlightTransLetter(self):
        #If it's not the last letter in current line 
        if self.trans_pos_counter < len(self.transcriptions[self.trans_current_line_number]):
            self.root.get_screen('MainMenu').ids.trans_text.text = f"[color=fcba03]{self.transcriptions[self.trans_current_line_number][self.trans_pos_counter]}[/color]{self.transcriptions[self.trans_current_line_number][self.trans_pos_counter+1:]}"
            self.trans_pos_counter += 1   
        #If it was the last letter
        if self.trans_pos_counter == len(self.transcriptions[self.trans_current_line_number]):
            self.trans_pos_counter = 0
            #If it's not the last line from available pool
            if self.trans_current_line_number < len(self.transcriptions):
                self.trans_current_line_number += 1
            #If it was the last line from available pool, go back to the beginning
            if self.trans_current_line_number == len(self.transcriptions):
                self.trans_current_line_number = 0
                
    #Method for displaying MDDialog with information about alphabets in Georgian alphabets'
    #history screen
    def history_screen_dialog(self,card_name,card_text,font_size):
        f_size = int(font_size)
        dialog_text = f"""[size={f_size}]
{self.language_strings[card_name][self.settings['language']]}

{self.language_strings[card_text][self.settings['language']]}
        [/size]"""
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
        self.ta_default_duration = self.language_strings['ta_duration'][self.settings['language']] + "\n" + str(self.ta_minutes_value)+':00'
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

    #Makes MDCards with colors in settings screen clickable/unclickable
    def color_tiles_unclickable(self,onOff):
        self.root.get_screen('MainMenu').ids.bg_one.disabled = onOff
        self.root.get_screen('MainMenu').ids.bg_two.disabled = onOff
        self.root.get_screen('MainMenu').ids.bg_three.disabled = onOff
        self.root.get_screen('MainMenu').ids.bg_four.disabled = onOff

    #Color of MDCards for choosing color in settings screen
    def tiles_background_colors(self,bg_type):
        tiles_bg = [(0.98,0.73,0.01,1),(0.11,0.85,0.98,1),(0.97,0.11,0.98,1),(0.22,0.04,0.04,1)]
        screen_bg = [(0.82,0.26,0.1,1),(0.31,0.24,0.78,1),(0.99,0.2,0.41,1)]
        
        if bg_type == 'tile':
            self.root.get_screen('MainMenu').ids.bg_one.md_bg_color = tiles_bg[0]
            self.root.get_screen('MainMenu').ids.bg_two.md_bg_color = tiles_bg[1]
            self.root.get_screen('MainMenu').ids.bg_three.md_bg_color = tiles_bg[2]
            self.root.get_screen('MainMenu').ids.bg_four.md_bg_color = tiles_bg[3]
            self.bg_color_type  = 'tile'
        if bg_type == 'screen':
            self.root.get_screen('MainMenu').ids.bg_one.md_bg_color = 0.4,0.73,0.2,1
            self.root.get_screen('MainMenu').ids.bg_two.md_bg_color = screen_bg[0]
            self.root.get_screen('MainMenu').ids.bg_three.md_bg_color = screen_bg[1]
            self.root.get_screen('MainMenu').ids.bg_four.md_bg_color = screen_bg[2]
            self.bg_color_type = 'screen'

    #Makes tiles with color selection visible in settings screen
    def colors_visible(self,bg_type):
        #Change MDCard color depending on whether it was clicked from tile
        #or screen background setting
        self.tiles_background_colors(bg_type)
        #Make MDCards with colors 'clickable'
        self.color_tiles_unclickable(False)
        self.root.get_screen('MainMenu').ids.bg_one.opacity = 1
        self.root.get_screen('MainMenu').ids.bg_two.opacity = 1
        self.root.get_screen('MainMenu').ids.bg_three.opacity = 1
        self.root.get_screen('MainMenu').ids.bg_four.opacity = 1

    #Method used after selecting tile background color in settings menu
    def select_color(self,color):
        #Make tiles with color selection 'unclickable'
        self.color_tiles_unclickable(True)
        #Makes tiles with color selection invisible in settings screen
        self.root.get_screen('MainMenu').ids.bg_one.opacity = 0
        self.root.get_screen('MainMenu').ids.bg_two.opacity = 0
        self.root.get_screen('MainMenu').ids.bg_three.opacity = 0
        self.root.get_screen('MainMenu').ids.bg_four.opacity = 0
        if self.bg_color_type =='tile':
            #Change color of currently selected tiles backround color in settings menu
            self.root.get_screen('MainMenu').ids.current_tile_bg_color.md_bg_color = color
            #Change value of variable with default tile background color
            self.default_card_color = color
            #Set new color value which will be saved to settings file
            self.settings['tile_bg_color_val'] = f"{color[0]},{color[1]},{color[2]},{color[3]}"
            #Change color of tiles in all screens
            #Letters learning mode
            self.root.get_screen('MainMenu').ids.geo_letter_card.md_bg_color = color
            self.root.get_screen('MainMenu').ids.first_letter.md_bg_color = color
            self.root.get_screen('MainMenu').ids.second_letter.md_bg_color = color
            self.root.get_screen('MainMenu').ids.third_letter.md_bg_color = color
            self.root.get_screen('MainMenu').ids.fourth_letter.md_bg_color = color
            #Time Atack mode
            self.root.get_screen('MainMenu').ids.ta_options.md_bg_color = color
            self.root.get_screen('MainMenu').ids.geo_letter_ta_card.md_bg_color = color
            #Transcription mode 
            self.root.get_screen('MainMenu').ids.transcription_stats.md_bg_color = color
            self.root.get_screen('MainMenu').ids.transcription_text_card.md_bg_color = color
            #History of Georgian alphabets screen
            self.root.get_screen('MainMenu').ids.history_screen_label.md_bg_color = color
            self.root.get_screen('MainMenu').ids.alph_general.md_bg_color = color
            self.root.get_screen('MainMenu').ids.alph_asomtavruli.md_bg_color = color
            self.root.get_screen('MainMenu').ids.alph_nuskhuri.md_bg_color = color
            self.root.get_screen('MainMenu').ids.alph_mkhedruli.md_bg_color = color
            #Settings screen
            self.root.get_screen('MainMenu').ids.settings_card.md_bg_color = color
            #Achievements screen
            self.root.get_screen('MainMenu').ids.achievement_ll1.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achievement_ll2.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achievement_ll3.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achievement_ta1.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achievement_ta2.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achievement_ta3.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achievement_trans1.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achievement_trans2.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achievement_trans3.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achievement_history.md_bg_color = color

        if self.bg_color_type == 'screen':
            #Change color of currently selected screen backround color in settings menu
            self.root.get_screen('MainMenu').ids.current_screen_bg_color.md_bg_color = color
            #Change value of variable with default screen background color
            self.screen_background_color = color
            #Set new color value which will be saved to settings file
            self.settings['screen_bg_color_val'] = f"{color[0]},{color[1]},{color[2]},{color[3]}"
            #Change screen background colors
            self.root.get_screen('MainMenu').ids.ll_background.md_bg_color = color
            self.root.get_screen('MainMenu').ids.ta_background.md_bg_color = color
            self.root.get_screen('MainMenu').ids.trans_background.md_bg_color = color
            self.root.get_screen('MainMenu').ids.hi_background.md_bg_color = color
            self.root.get_screen('MainMenu').ids.set_background.md_bg_color = color
            self.root.get_screen('MainMenu').ids.achi_background.md_bg_color = color
    
    #Displays achievement name and description in MDDialog when clicked in achievements screen
    def display_achievement_info(self,name,font_size):
        f_size = int(font_size)
        achievement_info = MDDialog(title= f'[size={f_size}]' + achievement_texts[name][self.settings['language']][0] + '[/size]',text=f'[size={f_size}]'+achievement_texts[name][self.settings['language']][1] + '[/size]')
        achievement_info.open()
    
    #Method saving status of achievements to achievement_status.csv file
    def save_achievements_status(self):
        with open('data/achievement_status.csv','w',encoding='utf8') as new_achievements_status:
                for achievement_name,values in self.achievements_status.items():
                    new_status = f'{achievement_name},{values[0]},{values[1]}\n'
                    new_achievements_status.write(new_status)

    #Method for checking conditions required to unlock achievements in Letter Learning mode
    def check_achievement_letters(self,letter):
        #If the correctly provided letters is not yet in the list
        if letter not in self.learned_letters:
            #Add it to the list
            self.learned_letters = self.learned_letters + letter
            self.achievements_status['achievement_letters'][1] = self.learned_letters
            #Increase number of correctly provided letters
            self.number_learned_letters +=1
            self.achievements_status['achievement_letters'][0] = str(self.number_learned_letters)
            #If the first achievement is unlocked
            if self.number_learned_letters == 10:
                achievement_letters_contrats = MDDialog(title=self.language_strings['achievement_unlocked'][self.settings['language']],text=achievement_texts['achievement_ll1'][self.settings['language']][0] + '\n\n' + achievement_texts['achievement_ll1'][self.settings['language']][1])
                achievement_letters_contrats.open()
                self.root.get_screen('MainMenu').ids.achievement_ll1.disabled = False
            #If the second achievement is unlocked
            if self.number_learned_letters == 20:
                achievement_letters_contrats = MDDialog(title=self.language_strings['achievement_unlocked'][self.settings['language']],text=achievement_texts['achievement_ll2'][self.settings['language']][0] + '\n\n' + achievement_texts['achievement_ll2'][self.settings['language']][1])
                achievement_letters_contrats.open()
                self.root.get_screen('MainMenu').ids.achievement_ll2.disabled = False
            #If the third achievement is unlocked
            if self.number_learned_letters == 33:
                achievement_letters_contrats = MDDialog(title=self.language_strings['achievement_unlocked'][self.settings['language']],text=achievement_texts['achievement_ll3'][self.settings['language']][0] + '\n\n' + achievement_texts['achievement_ll3'][self.settings['language']][1])
                achievement_letters_contrats.open()
                self.achievement_ll3_notclickable = False
                self.root.get_screen('MainMenu').ids.achievement_ll3.disabled = False
            #Update file with current data
            self.save_achievements_status()

    #Method for checking conditions required to unlock achievements in Time Attack mode
    def check_achievement_ta(self):
        #Achievement for 10 correct answers in Time Attack mode
        if self.answer_streak_score_ta >= 10 and self.achievements_status['achievement_time_attack'][0] == '0':
            self.achievements_status['achievement_time_attack'][0] = '1'
            achievement_time_attack_10 = MDDialog(title=self.language_strings['achievement_unlocked'][self.settings['language']],text=achievement_texts['achievement_ta1'][self.settings['language']][0] + '\n\n' + achievement_texts['achievement_ta1'][self.settings['language']][1])
            achievement_time_attack_10.open()
            self.root.get_screen('MainMenu').ids.achievement_ta1.disabled = False
            self.save_achievements_status()
        #Achievement for 20 correct answers in Time Attack mode
        if self.answer_streak_score_ta >= 20 and self.achievements_status['achievement_time_attack'][0] == '1':
            self.achievements_status['achievement_time_attack'][0] = '2'
            achievement_time_attack_20 = MDDialog(title=self.language_strings['achievement_unlocked'][self.settings['language']],text=achievement_texts['achievement_ta2'][self.settings['language']][0] + '\n\n' + achievement_texts['achievement_ta2'][self.settings['language']][1])
            achievement_time_attack_20.open()
            self.root.get_screen('MainMenu').ids.achievement_ta2.disabled = False
            self.save_achievements_status()
        #Achievement for 30 correct answers in Time Attack mode
        if self.answer_streak_score_ta >= 20 and self.achievements_status['achievement_time_attack'][0] == '2':
            self.achievements_status['achievement_time_attack'][0] = '3'
            achievement_time_attack_30 = MDDialog(title=self.language_strings['achievement_unlocked'][self.settings['language']],text=achievement_texts['achievement_ta3'][self.settings['language']][0] + '\n\n' + achievement_texts['achievement_ta3'][self.settings['language']][1])
            achievement_time_attack_30.open()
            self.root.get_screen('MainMenu').ids.achievement_ta3.disabled = False
            self.save_achievements_status()            

    #Method for checking conditions required to achieve history achievement.
    def check_achievement_history(self,tile_name):
        #Check if the tiles in History screen were clicked before
        if tile_name == 'alph_general':
           if  self.achievements_status['achievement_history'][1][0] == '0':
               self.achievements_status['achievement_history'][1] = 'g'+self.achievements_status['achievement_history'][1][1:]
        if tile_name == 'alph_asomtavruli':
           if  self.achievements_status['achievement_history'][1][1] == '0':
               self.achievements_status['achievement_history'][1] = self.achievements_status['achievement_history'][1][0] + 'a'+ self.achievements_status['achievement_history'][1][2:]
        if tile_name == 'alph_nuskhuri':
           if  self.achievements_status['achievement_history'][1][2] == '0':
               self.achievements_status['achievement_history'][1] = self.achievements_status['achievement_history'][1][0:2] + 'n' + self.achievements_status['achievement_history'][1][3]
        if tile_name == 'alph_mkhedruli':
           if  self.achievements_status['achievement_history'][1][3] == '0':
               self.achievements_status['achievement_history'][1] = self.achievements_status['achievement_history'][1][0:3] + 'm'
        #If the achievement wasn't achieved yet
        if self.achievements_status['achievement_history'][0] == '0':
            #Check if all tiles were clicked
            if self.achievements_status['achievement_history'][1] == 'ganm':
                #If yes change achievement status and display congratulations message
                self.achievements_status['achievement_history'][0] = '1'
                achievement_history_congrats = MDDialog(title=self.language_strings['achievement_unlocked'][self.settings['language']],text=achievement_texts['achievement_history'][self.settings['language']][0] + '\n\n' + achievement_texts['achievement_history'][self.settings['language']][1]) 
                achievement_history_congrats.open()
                self.root.get_screen('MainMenu').ids.achievement_history.disabled = False
        #Save the achievement status to file
        self.save_achievements_status()
                
    def test(self,type):
        print(type)

Mkhedruli().run()

