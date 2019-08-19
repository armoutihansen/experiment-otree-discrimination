from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from django.utils.translation import ugettext as _


# variables for all templates
# --------------------------------------------------------------------------------------------------------------------
def vars_for_all_templates(self):
    return {
        'lottery_lo':  c(Constants.lottery_lo),
        'lottery_hi':  c(Constants.lottery_hi),
        'probability': "{0:.1f}".format(Constants.probability) + "%",
        'decision_d': Constants.decision_d
    }


# ******************************************************************************************************************** #
# *** CLASS INSTRUCTIONS *** #
# ******************************************************************************************************************** #
class InstructionsGerman(Page):

    # only display instruction in round 1
    # ----------------------------------------------------------------------------------------------------------------
    def is_displayed(self):
        return self.subsession.round_number == 1


# ******************************************************************************************************************** #
# *** PAGE DECISION *** #
# ******************************************************************************************************************** #
class DecisionGerman(Page):

    # form model
    # ----------------------------------------------------------------------------------------------------------------
    form_model = 'player'

    # form fields
    # ----------------------------------------------------------------------------------------------------------------
    def get_form_fields(self):

        # unzip list of form_fields from <cem_choices> list
        form_fields = [list(t) for t in zip(*self.participant.vars['cem_choices'])][1]

        # provide form field associated with pagination or full list
        if Constants.one_choice_per_page:
            page = self.subsession.round_number
            return [form_fields[page - 1]]
        else:
            return form_fields

    # variables for template
    # ----------------------------------------------------------------------------------------------------------------
    def vars_for_template(self):

        # specify info for progress bar
        total = Constants.num_choices
        page = self.subsession.round_number
        progress = page / total * 100

        if Constants.one_choice_per_page:
            return {
                'page':      page,
                'total':     total,
                'progress':  progress,
                'choices':   [self.player.participant.vars['cem_choices'][page-1]]
            }
        else:
            return {
                'choices':   self.player.participant.vars['cem_choices']
            }

    # set payoff, determine consistency, and set switching row
    # ----------------------------------------------------------------------------------------------------------------
    def before_next_page(self):

        # unzip indices and form fields from <cem_choices> list
        round_number = self.subsession.round_number
        form_fields = [list(t) for t in zip(*self.participant.vars['cem_choices'])][1]
        indices = [list(t) for t in zip(*self.participant.vars['cem_choices'])][0]
        index = indices[round_number - 1]

        # if choices are displayed sequentially
        # ------------------------------------------------------------------------------------------------------------
        if Constants.one_choice_per_page:

            # replace current choice in <choices_made>
            current_choice = getattr(self.player, form_fields[round_number - 1])
            self.participant.vars['cem_choices_made'][index - 1] = current_choice

            # if current choice equals index to pay ...
            if index == self.player.participant.vars['cem_index_to_pay']:
                # set payoff
                self.player.set_payoffs()

            # after final choice
            if round_number == Constants.num_choices:
                # determine consistency
                self.player.set_consistency()
                # set switching row
                self.player.set_switching_row()

        # if choices are displayed in tabular format
        # ------------------------------------------------------------------------------------------------------------
        if not Constants.one_choice_per_page:

            # replace choices in <choices_made>
            for j, choice in zip(indices, form_fields):
                choice_i = getattr(self.player, choice)
                self.participant.vars['cem_choices_made'][j - 1] = choice_i

            # set payoff
            self.player.set_payoffs()
            # determine consistency
            self.player.set_consistency()
            # set switching row
            self.player.set_switching_row()


# ******************************************************************************************************************** #
# *** PAGE CONTROL QUESTION MPL *** #
# ******************************************************************************************************************** #
class ControlQuestions(Page):
    form_model = 'player'
    form_fields = ['mpl_question_1', 'mpl_question_2']

    def error_message(self, values):
        if values['mpl_question_1'] != 4:
            return "Das Ergebnis der ersten Frage ist nicht richtig"
        if values['mpl_question_2'] != 2:
            return "Das Ergebnis der zweiten Frage ist nicht richtig"


# ******************************************************************************************************************** #
# *** PAGE SEQUENCE *** #
# ******************************************************************************************************************** #
page_sequence = [ControlQuestions, DecisionGerman]

if Constants.instructions:
    page_sequence.insert(0, InstructionsGerman)