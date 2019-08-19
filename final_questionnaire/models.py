from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

from otree_tools.models.fields import OtherModelField

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'final_questionnaire'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    age = models.IntegerField(label="Wie alt sind Sie?")
    gender = models.IntegerField(choices=[[1, 'Männlich'], [2, 'Weiblich'], [3, 'Divers']],label="Was ist Ihr Geschlecht?",widget=widgets.RadioSelect)
    sibling_number = models.IntegerField(label="Wie viele Geschwister haben Sie?")
    program = models.CharField(label="Welchen Studiengang belegen Sie?")
    grad_or_undergrad_choices = (
        ('Bachelor', 'Bachelor'),
        ('Master', 'Master'))
    graduate_or_undergraduate = models.CharField(choices=grad_or_undergrad_choices,label='Studieren Sie im Bachelor oder im Master?',widget=widgets.RadioSelect)
    year_of_program = models.IntegerField(label="Im wievielten Semester Ihres aktuellen Studiums befinden Sie sich?")
    previous_experiments = OtherModelField(choices=['Nein'],label="Haben Sie vorher jemals an ökonomischen oder psychologischen Experimenten teilgenommen?",other_label='Ja (Bitte geben Sie an wie häufig)',other_value='Ja_', blank=True)
    importance_of_religion = models.IntegerField(label="Auf einer Skala von 0 (Überhaupt nicht wichtig) bis 10 (sehr wichtig), wie wichtig ist Religion in Ihrem Leben?",widget=widgets.Slider(show_value=True,attrs={'min': 0, 'max': 10,'step': 1}))
    nationality = models.CharField(choices = ['Deutsch','Nicht-Deutsch'],label='Was ist Ihre Nationalität?',widget=widgets.RadioSelect)
    volunteer_work = OtherModelField(choices=['Nein'],label="Haben Sie in den letzten 12 Monaten ehrenamtlich für Hochschulgruppen, Vereine oder andere gemeinnützige Organisationen gearbeitet?",other_label='Ja (Bitte geben Sie an wie viele Stunden Sie dort insgesamt gearbeitet haben)',other_value='Ja_', blank=True)
    helpfulness_of_communication = models.IntegerField(label="Auf einer Skala von 0 (Überhaupt nicht hilfreich) bis 10 (äußerst hilfreich), bewerten Sie bitte wie hilfreich Sie die Kommunikation mit Ihren Gruppenmitgliedern empfunden haben um die beiden extra Fragen bezüglich der Bilder zu beantworten",widget=widgets.Slider(show_value=True,attrs={'class' : 'helpfulness_of_communication', 'min': 0, 'max': 10,'step': 1}))
    attachment_level = models.IntegerField(label="Auf einer Skala von 0 (überhaupt nicht verbunden) bis 10 (äußerst verbunden), bewerten Sie bitte, wie eng Sie sich während des gesamten Experiments mit Ihrer eigenen Gruppe verbunden gefühlt haben",widget=widgets.Slider(show_value=True,attrs={'min': 0, 'max': 10, 'step': 1}))
    ease_of_instruction = models.IntegerField(label="Auf einer Skala von 0 (überhaupt nicht einfach) bis 10 (äußerst einfach), wie einfach konnten Sie den Instruktionen folgen und die Aufgaben im Experiment erledigen?",widget=widgets.Slider(show_value=True,attrs={'min': 0, 'max': 10,'step': 1}))
    hard_to_follow_instructions = models.TextField(label="Gab es irgendwelche Instruktionen die Sie schwer verstanden haben? Wenn ja, listen Sie diese bitte auf.",blank=True)
    familiarity_with_klee = models.IntegerField(label="Bitte bewerten Sie auf einer Skala von 0 (überhaupt nicht vertraut) bis 10 (äußerst vertraut), wie vertraut Sie mit den Gemälden von Klee vor diesem Experiment waren.",widget=widgets.Slider(show_value=True,attrs={'min': 0, 'max': 10,'step': 1}))
    familiarity_with_kandinsky = models.IntegerField(label="Bitte bewerten Sie auf einer Skala von 0 (überhaupt nicht vertraut) bis 10 (äußerst vertraut), wie vertraut Sie mit den Gemälden von Kandinsky vor diesem Experiment waren.",widget=widgets.Slider(show_value=True,attrs={'min': 0, 'max': 10,'step': 1}))
    dictator_strategy_no_risk_choices = (
        ('equally', 'a) Versuch, Punkte gleichmäßig zwischen beiden aufteilen.'),
        ('more_to_own_group','b) Versuch, dem Teilnehmer Ihrer eigenen Gruppe mehr Punkte zuzuteilen.'),
        ('more_to_other_group','c) Versuch, dem Teilnehmer der anderen Gruppe mehr Punkte zuzuteilen.'),
        ('random','d) Zufällig.'))
    dictator_strategy_risk_choices = (
        ('equally', 'a) Versuch, Punkte gleichmäßig zwischen beiden aufteilen.'),
        ('more_to_own_group','b) Versuch, dem Teilnehmer Ihrer eigenen Gruppe mehr Punkte zuzuteilen.'),
        ('more_to_other_group','c) Versuch, dem Teilnehmer der anderen Gruppe mehr Punkte zuzuteilen.'),
        ('maximise_my_earning','d) Versuch, unter Berücksichtigung des Risikos Ihre Auszahlung zu erhöhen.'),
        ('both_a_and_d','e) Sowohl a) als auch d).'),
        ('both_b_and_d','f) Sowohl b) als auch d).'),
        ('both_c_and_d','g) Sowohl c) als auch d).'),
        ('random','h) Zufällig.'))
    dictator_strategy_no_risk = OtherModelField(label='Im zweiten Teil des Experiments sollten Sie Punkte zwischen den anderen beiden Teilnehmern verteilen und waren keinem Risiko bezüglich Ihrer eigenen Zuteilung ausgesetzt, wie würden Sie die von Ihnen angewendete Strategie beschreiben?',choices= dictator_strategy_no_risk_choices, other_label='e) Sonstige (Bitte spezifizieren Sie)', blank=True)
    dictator_strategy_risk = OtherModelField(label="Im zweiten Teil des Experiments sollten Sie Punkte zwischen den anderen beiden Teilnehmern verteilen und waren einem Risiko bezüglich Ihrer eigenen Zuteilung ausgesetzt, wie würden Sie die von Ihnen angewendete Strategie beschreiben?",choices=dictator_strategy_risk_choices,other_label='i) Sonstige (Bitte spezifizieren Sie)', blank=True)
    group_dynamic_influence = models.TextField(label="Wie hat die Gruppendynamik Ihre Entscheidungen insgesamt beeinflusst?")
    payoff = models.FloatField()
    payoff_in_euros = models.FloatField()
    f_p = models.FloatField()
