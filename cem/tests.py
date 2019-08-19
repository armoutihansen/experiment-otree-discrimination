from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants
import random


# **********************************************************************************************************************
# *** BOT
# **********************************************************************************************************************
class PlayerBot(Bot):

    def play_round(self):

        # define page as round_number
        page = self.subsession.round_number

        # get bot's switching point
        switching_point = self.player.participant.vars['cem-bot_switching_point']

        # ------------------------------------------------------------------------------------------------------------ #
        # submit instructions page
        # ------------------------------------------------------------------------------------------------------------ #
        if Constants.instructions:
            if Constants.one_choice_per_page:
                if page == 1:
                    yield (pages.Instructions)
            else:
                yield (pages.InstructionsGerman)

        yield (pages.ControlQuestions, {'mpl_question_1': 4, 'mpl_question_2': 2})

        # ------------------------------------------------------------------------------------------------------------ #
        # make decisions
        # ------------------------------------------------------------------------------------------------------------ #
        indices = [list(t) for t in zip(*self.player.participant.vars['cem_choices'])][0]
        form_fields = [list(t) for t in zip(*self.player.participant.vars['cem_choices'])][1]

        if Constants.one_choice_per_page:
            if indices[page - 1] <= switching_point:
                yield (pages.DecisionGerman, {
                    form_fields[page - 1]: 'A'
                })
            else:
                yield (pages.DecisionGerman, {
                    form_fields[page - 1]: 'B'
            })

        else:
            decisions = []
            for i in indices:
                if i <= switching_point:
                    decisions.append('A')
                else:
                    decisions.append('B')

            choices = zip(form_fields, decisions)
            yield (pages.DecisionGerman, {
                i: j for i, j in choices
            })
