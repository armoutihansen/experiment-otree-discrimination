from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

#OTree uses classes to track each page in the page_sequence, each class has the same name as the 
#HTML file. 

class LandingPageGerman(Page):
    pass

class NDAGerman(Page):
    pass

class InstructionsGerman(Page):
    pass

class DoNotTalkPageGerman(Page):
    pass

class FirstPhoto(Page):
    '''
    Basically used to pass the form into the HTML using the model defined in Player in models.py
    We can pick which attributes we want to pass onto the page.
    '''
    form_model = 'player'
    form_fields = ['level1']

class SecondPhoto(Page):
    form_model = 'player'
    form_fields = ['level2']

class ThirdPhoto(Page):
    form_model = 'player'
    form_fields = ['level3']

class FourthPhoto(Page):
    form_model = 'player'
    form_fields = ['level4']

class FifthPhoto(Page):
    form_model = 'player'
    form_fields = ['level5']

class TransitionTo2German(Page):
    def vars_for_template(self):
        all_players = self.subsession.get_players()
        group_players = int(len(all_players)/2)
        return {'group_players':group_players, 'group': self.participant.vars['group']}
    pass

class Matching(WaitPage):
    title_text = "Bildung der Gruppen"
    body_text = "Die Gruppen werden nun gebildet. Bitte warten Sie."
    def after_all_players_arrive(self):
        '''All the functions defined in models.py are called here'''
        players = self.subsession.get_players()
        self.subsession.grouping_players(players)
        self.subsession.making_dictators(players)
        self.subsession.dictator_sequences(players)
        self.subsession.match(players)


#Control Question Pages#
class ControlPage1(Page):
    form_model = 'player'
    form_fields = ['percentage_question_1', 'percentage_question_2', 'average_question_1', 'average_question_2']

    def error_message(self, values):
        if values['percentage_question_1'] != 6.5:
            return "Das Ergebnis der ersten Frage ist nicht richtig"
        if values['percentage_question_2'] != 4:
            return "Das Ergebnis der zweiten Frage ist nicht richtig"
        if values['average_question_1'] != 35:
            return "Das Ergebnis der dritten Frage ist nicht richtig"
        if values['average_question_2'] != 40:
            return "Das Ergebnis der vierten Frage ist nicht richtig"


class ControlPage2(Page):
    form_model = 'player'
    form_fields = ['lottery_question_1', 'lottery_question_2']

    def error_message(self, values):
        if values['lottery_question_1'] != 70:
            return "Das Ergebnis der fünften Frage ist nicht richtig"
        if values['lottery_question_2'] != 1:
            return "Das Ergebnis der sechsten Frage ist nicht richtig"


page_sequence = [
    LandingPageGerman,
    DoNotTalkPageGerman,
    NDAGerman,
    ControlPage1,
    ControlPage2,
    InstructionsGerman,
    FirstPhoto,
    SecondPhoto,
    ThirdPhoto,
    FourthPhoto,
    FifthPhoto,
    Matching,
    TransitionTo2German,
]
