from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otree_tools.utils import get_time_per_page
from random import shuffle
import copy
import collections, random

class DS(WaitPage):

    def after_all_players_arrive(self):
        '''
        First page that sets active treatments and active receivers. This is just boilerplate stuff
        to prepare for the treatments themselves.
        '''
        players = self.group.get_players()
        for player in players:
            if player.participant.vars['dictator']:
                player.participant.vars['active_treatment'] = player.participant.vars['dictator_sequence'][player.round_number-1]
                player.participant.vars['active_kandinsky_receiver'] = player.participant.vars['kandinsky_receivers_list'][player.round_number-1]
                player.participant.vars['active_klee_receiver'] = player.participant.vars['klee_receivers_list'][player.round_number-1]
            else:
                player.participant.vars['active_treatment'] = player.participant.vars['dictator_sequence'][player.round_number-1]
            player.active_treatment = player.participant.vars['active_treatment']


class IPageGerman(Page):
    '''
    Instruction page for dictators which is only displayed in the beginning.
    '''
    def vars_for_template(self):
        return {'group':self.player.participant.vars['group']}

    def is_displayed(self):
        return self.player.participant.vars['dictator']==True and self.player.round_number == 1

class RIPageGerman(Page):
    '''
    Instruction page for receivers, which is again only displayed in the beginning.
    '''
    def vars_for_template(self):
        return {'group':self.player.participant.vars['group']}

    def is_displayed(self):
        return self.player.participant.vars['dictator']==False and self.player.round_number == 1

class T1German(Page):
    '''
    Class for Treatment 1, only displayed when active_treatment is 1.
    '''
    def vars_for_template(self):
        return {'group':self.player.participant.vars['group']}

    def is_displayed(self):
        return self.player.participant.vars['active_treatment'] == 1

    form_model = 'player'

    def get_form_fields(self):
        all_formfields = [self.player.first_field, self.player.second_field]
        if not self.player.shuffle_happened:
            shuffle(all_formfields)
            self.player.shuffle_happened = True
            self.player.first_field = all_formfields[0]
            self.player.second_field = all_formfields[1]
        return all_formfields

    def error_message(self, values):
        if values["ingroup_offer"] + values["outgroup_offer"] != 100:
            return 'Die Punkte müssen sich zu 100 summieren'

    def before_next_page(self):
        self.player.time_spent = str(get_time_per_page(self.player, 'T1German'))
        self.player.self_offer = (self.player.ingroup_offer + self.player.outgroup_offer)//2 
        #Sets self_offer to the average of the two inputs,as per specification

class T2German(Page):
    '''
    Class for Treatment 2, only displayed when active_treatment = 2
    '''
    def vars_for_template(self):
        return {'group':self.player.participant.vars['group']}

    def is_displayed(self): 
        return self.player.participant.vars['active_treatment'] == 2

    form_model = 'player'

    def get_form_fields(self):
        all_formfields = [self.player.first_field, self.player.second_field]
        if not self.player.shuffle_happened:
            shuffle(all_formfields)
            self.player.shuffle_happened = True
            self.player.first_field = all_formfields[0]
            self.player.second_field = all_formfields[1]
        return all_formfields

    def error_message(self, values):
        if values["ingroup_offer"] + values["outgroup_offer"] != 100:
            return 'Die Punkte müssen sich zu 100 summieren'

    def before_next_page(self):
        options_to_choose_from = [self.player.ingroup_offer, self.player.outgroup_offer]
        self.player.self_offer = random.choice(options_to_choose_from)
        #Picks one of the two offers randomly but with equal probability
        self.player.time_spent = str(get_time_per_page(self.player, 'T2German'))


class PTPage(WaitPage):
    '''
    The Post-Treatment page, which deals with calculating payoffs for everyone after each 
    treatment. 
    It does this by first setting the payoff of the dictator by appending to a payoff_array,
    else it sets a receiver, finds the dictator that has that receiver, and appends the 
    receiver payoff to a payoff array too. At the end of the 2nd round, once everyone has 
    gone through two treatments, one of the two payoffs from the payoff array is selected, with
    equal probability.
    '''
    def after_all_players_arrive(self):
        all_players = self.subsession.get_players()
        for some_player in all_players: #painful variable choice but w/e
            if some_player.participant.vars['dictator']:
                payoff_dictator = some_player.self_offer
                some_player.participant.vars['payoff_array'].append(payoff_dictator)
            else:
                player_id = some_player.participant.vars["player_id"]
                player_payoff = 0
                for player in self.subsession.get_players():
                    if player.participant.vars['dictator']: # First we check active receivers to check if the player was involved, and if they were we check color to see if we have to count their ingroup or outgroup offer
                        if (player.participant.vars["active_klee_receiver"] == player_id or player.participant.vars["active_kandinsky_receiver"] == player_id) and some_player.participant.vars["group"] == player.participant.vars["group"]:
                            some_player.participant.vars['payoff_array'].append(player.ingroup_offer)
                        elif (player.participant.vars["active_klee_receiver"] == player_id or player.participant.vars["active_kandinsky_receiver"] == player_id) and some_player.participant.vars["group"] != player.participant.vars["group"]:
                            some_player.participant.vars['payoff_array'].append(player.outgroup_offer)
            if(some_player.round_number == 2):
                some_player.participant.vars['the_dictator_payoff'] = random.choice(some_player.participant.vars['payoff_array'])
                some_player.payoff = some_player.participant.vars['the_dictator_payoff']

page_sequence = [
    DS,
    IPageGerman,
    RIPageGerman,
    T1German,
    T2German,
    PTPage,
]
