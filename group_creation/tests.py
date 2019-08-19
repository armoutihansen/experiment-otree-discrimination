from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):
        '''Pretty self explanatory'''
        yield(pages.LandingPageGerman)
        yield(pages.DoNotTalkPageGerman)
        yield(pages.NDAGerman)
        yield (pages.ControlPage1, {'average_question_1': 35,
                                    'average_question_2': 40,
                                    'percentage_question_1': 6.5,
                                    'percentage_question_2': 4})
        yield (pages.ControlPage2, {'lottery_question_1': 70,
                                    'lottery_question_2': 1})
        yield(pages.InstructionsGerman)
        yield (pages.FirstPhoto, {'level1':random.randint(0,100)})
        yield (pages.SecondPhoto, {'level2':random.randint(0,100)})
        yield (pages.ThirdPhoto, {'level3':random.randint(0,100)})
        yield (pages.FourthPhoto, {'level4':random.randint(0,100)})
        yield (pages.FifthPhoto, {'level5':random.randint(0,100)})
        yield(pages.TransitionTo2German)
