from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
The Dictator puts the user through two treatments, regardless of whether they're a dictator or a
receiver.
"""
 

class Constants(BaseConstants):
    '''
    Same idea as in the previous applications
    '''
    name_in_url = 'the_dictator'
    players_per_group = None
    num_rounds = 2
    fields_and_styling_template = 'the_dictator/fields_and_styling_German.html'
    header_template = 'the_dictator/stylesheets_and_header_German.html'
    submit_button_template = 'group_creation/submit_button.html'



class Subsession(BaseSubsession):
    def creating_session(self):
        for p in self.get_players():
            p.shuffle_happened = False
            p.first_field = 'ingroup_offer'
            p.second_field = 'outgroup_offer'


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    '''
    Same as the constants docstring above
    '''
    self_offer = models.CurrencyField(label = 'Amount to yourself:',min=0) 
    ingroup_offer = models.CurrencyField(label= 'Punkte für den Teilnehmer aus Ihrer Gruppe:',min=0)
    outgroup_offer = models.CurrencyField(label= 'Punkte für den Teilnehmer aus der anderen Gruppe:',min=0)
    active_treatment = models.IntegerField()
    total = models.CurrencyField(blank=True)
    time_spent = models.StringField()
    shuffle_happened = models.BooleanField()
    first_field = models.StringField()
    second_field = models.StringField()

