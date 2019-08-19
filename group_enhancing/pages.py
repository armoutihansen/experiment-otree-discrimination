from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import copy, bisect

#Change this value to whatever amount of points you want to set for correct answer
TOTAL_POINTS = 5

def get_team(player):
    '''
    Gets the group in which the player is and returns it
    '''
    if (player.participant.vars['group']=='Klee'):
        return 'Klee'
    else:
        return 'Kandinsky'

def get_chat_channel(player):
    '''
    Returns part of the chat channel which needs to be set for each group.
    '''
    return get_team(player)

class InstructionsGerman(Page):
    def vars_for_template(self):
        return {'total_points': TOTAL_POINTS, 'group':get_team(self.player)}

    def is_displayed(self):
        return self.round_number == 1 #Only display in the beginning

class FirstPaintingGuess2German(Page):

    def vars_for_template(self):
        return {'chat_channel': get_chat_channel(self.player)+'_Channel_1','artist_group':get_team(self.player)} 
        #Construct chat channel in a sort of hacky way by appending Channel_1 to group name

    form_model = 'player'
    form_fields = ['first_painting']

    def before_next_page(self):
        cleaned_input = self.player.first_painting.lower() #Clean the input by converting to lowercase
        if(cleaned_input == 'klee'): #If correct, give points
            self.player.participant.vars['group_enhancing_payoff'].append(TOTAL_POINTS)
            self.player.payoff_1 = TOTAL_POINTS
        else:
            self.player.participant.vars['group_enhancing_payoff'].append(0)
            self.player.payoff_1 = 0
        self.player.participant.vars['painting_guesses'] = [self.player.first_painting]

    timeout_seconds = 300 #Timeout the page in 5 minutes(or 300 seconds)
    

class SecondPaintingGuess2German(Page):
    '''
    Same idea as FirstPaintingGuess, except with a bunch of 2s instead of 1s.
    '''

    def vars_for_template(self):
        return {'chat_channel': get_chat_channel(self.player)+'_Channel_2','artist_group':get_team(self.player)}

    form_model = 'player'
    form_fields = ['second_painting']

    timeout_seconds = 300

    def before_next_page(self):
        cleaned_input = self.player.second_painting.lower()
        if(cleaned_input == 'kandinsky'):
            self.player.participant.vars['group_enhancing_payoff'].append(TOTAL_POINTS)
            self.player.payoff_2 = TOTAL_POINTS
        else:
            self.player.participant.vars['group_enhancing_payoff'].append(0)
            self.player.payoff_2 = 0
        self.player.participant.vars['painting_guesses'].append(self.player.second_painting)
        self.player.payoff = self.player.payoff_1 + self.player.payoff_2

class WaitForPlayersPage(WaitPage):

    def after_all_players_arrive(self):
        pass

page_sequence = [
    InstructionsGerman,
    WaitForPlayersPage,
    FirstPaintingGuess2German,
    WaitForPlayersPage,
    SecondPaintingGuess2German,
    WaitForPlayersPage,
]
