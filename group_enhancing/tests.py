from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random

class PlayerBot(Bot):

    def play_round(self):
        if self.player.round_number == 1:
        	yield(pages.InstructionsGerman)
        choices = ['Klee', 'Kandinsky']
        yield (pages.FirstPaintingGuess2German, {'first_painting':random.choice(choices)})
        yield (pages.SecondPaintingGuess2German, {'second_painting':random.choice(choices)})