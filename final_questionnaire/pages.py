from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants,Player


class QuestionnairePage(Page):
    form_model = 'player'
    form_fields = ['age', 'gender', 'sibling_number', 'program', 'graduate_or_undergraduate','year_of_program',
                   'previous_experiments','importance_of_religion','nationality','volunteer_work',
                   'helpfulness_of_communication','attachment_level','dictator_strategy_no_risk',
                   'dictator_strategy_risk','group_dynamic_influence','familiarity_with_klee',
                   'familiarity_with_kandinsky','ease_of_instruction','hard_to_follow_instructions']
#    def get_form_fields(self):
      #  if self.player.participant.vars['dictator']:
#            return ['age', 'gender', 'sibling_number', 'program', 'graduate_or_undergraduate','year_of_program','previous_experiments','importance_of_religion','nationality','volunteer_work',
#                    'helpfulness_of_communication','attachment_level','dictator_strategy_no_risk','dictator_strategy_risk','group_dynamic_influence','familiarity_with_klee','familiarity_with_kandinsky','ease_of_instruction','hard_to_follow_instructions']
       # else:
        #    return ['age', 'gender', 'sibling_number', 'program', 'graduate_or_undergraduate','year_of_program','previous_experiments','importance_of_religion','nationality','volunteer_work',
         #           'helpfulness_of_communication','attachment_level','group_dynamic_influence','familiarity_with_klee','familiarity_with_kandinsky','ease_of_instruction','hard_to_follow_instructions']

class Results(Page):
    def vars_for_template(self):
        final_payoff = 0
        participation_fee = self.session.config['participation_fee']
#        final_payoff = participation_fee + int(self.participant.vars['cem_payoff']) + int(self.participant.vars['the_dictator_payoff']) + int(self.participant.vars['group_enhancing_payoff'][0]) + int(self.participant.vars['group_enhancing_payoff'][1])
#        self.player.payoff = int(final_payoff)
#        self.player.payoff_in_euros = final_payoff/100
        return {'final_payoff': self.participant.payoff,'participation_fee': participation_fee, 'payoff_in_euros': self.participant.payoff_plus_participation_fee(), 'c_t_p': self.participant.vars['cem_choice_to_pay'][7:]}

    def before_next_page(self):
        self.player.f_p = float(self.participant.payoff_plus_participation_fee())

class FinalPage(Page):
    pass


class Wait(WaitPage):
    pass

page_sequence = [
    QuestionnairePage,
    Wait,
    Results,
    FinalPage,
]
