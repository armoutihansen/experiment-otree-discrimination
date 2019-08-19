from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):
        if self.player.round_number == 1:
            if (self.player.participant.vars['dictator'] == True):
                yield(pages.IPageGerman)
            else:
                yield(pages.RIPageGerman)
        if self.player.participant.vars['active_treatment'] == 1:
            first_offer = random.randint(0,100)
            second_offer = 100 - first_offer
            yield(pages.T1German, {'ingroup_offer' : first_offer, 'outgroup_offer' : second_offer})
        elif self.player.participant.vars['active_treatment'] == 2:
            first_offer = random.randint(0,100)
            second_offer = 100 - first_offer
            yield(pages.T2German, {'ingroup_offer' : first_offer, 'outgroup_offer' : second_offer})

