from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from typing import (List, Dict)
import random
import itertools

author = 'Your name here'

doc = """
Group Enhancing gives two paintings, asking the user to guess which artist painted them. Users
can chat with people in their own group before submitting an answer.
"""


class Constants(BaseConstants):
    '''
    Class that defines constants that are accessible all across the application
    '''
    name_in_url = 'group_enhancing'
    players_per_group = None
    num_rounds = 1
    modal_and_misc_template = 'group_enhancing/modal_and_miscellanous_German.html'
    submit_button_template = 'group_creation/submit_button.html'
    instructions_and_chat_template = 'group_enhancing/chat_and_form_2_German.html'


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    '''
    Class that defines all the things we'll be storing in the database.
    '''
    color = models.StringField()
    artist_choices = (
    ('Klee', 'Klee'),
    ('Kandinsky', 'Kandinsky'))
    first_painting = models.CharField(choices=artist_choices, label=False, widget=widgets.RadioSelect)
    second_painting = models.CharField(choices=artist_choices, label=False, widget=widgets.RadioSelect)
    payoff_1 = models.CurrencyField()
    payoff_2 = models.CurrencyField()
