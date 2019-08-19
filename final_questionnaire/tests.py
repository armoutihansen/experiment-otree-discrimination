from otree.api import Currency as c, currency_range, Submission
from . import pages
from ._builtin import Bot
from .models import Constants
import random


class PlayerBot(Bot):

    def play_round(self):
        yield (pages.QuestionnairePage, {'age': random.randint(0, 100),
                                        'gender': random.randint(1, 3),
                                        'sibling_number': random.randint(0, 5),
                                        'program': 'N/A',
                                        'graduate_or_undergraduate': random.choice(('Bachelor','Master')),
                                        'year_of_program': random.randint(0, 10),
#                                        'previous_experiments': 'Nein',
                                        'importance_of_religion': random.randint(0, 10),
                                        'nationality': random.choice(('Deutsch', 'Nicht-Deutsch')),
#                                        'volunteer_work': 'Nein',
                                        'helpfulness_of_communication': random.randint(0, 10),
                                        'attachment_level': random.randint(0, 10),
                                        'ease_of_instruction': random.randint(0, 10),
                                        'familiarity_with_klee': random.randint(0, 10),
                                        'familiarity_with_kandinsky': random.randint(0, 10),
                                        'group_dynamic_influence': 'hello'})
#                                        'dictator_strategy_no_risk': 'a) Versuch, Punkte gleichmäßig zwischen beiden aufteilen.',
#                                        'dictator_strategy_risk': 'a) Versuch, Punkte gleichmäßig zwischen beiden aufteilen.'})
        yield(pages.Results)
        yield Submission(pages.FinalPage, check_html=False)

