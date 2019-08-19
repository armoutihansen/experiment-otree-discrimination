
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import statistics
from random import shuffle,choice,randint
import itertools

author = 'Your name here'

doc = """
Group Creation collects the user input on 5 different paintings using a slider, then splits
the users into two groups based on that input. Furthermore, it subdivides the groups into dictators
and receivers, setting up for the group_enhancing application.
"""


class Constants(BaseConstants):
    '''
    Class to define constants that can be called anywhere on the application
    '''
    name_in_url = 'group_creation'
    players_per_group = None
    num_rounds = 1
    instructions_and_style_template = 'group_creation/instructions_and_style_German.html'
    submit_button_template = 'group_creation/submit_button.html'

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    '''
    Class used to define the things that need to be stored in the database and parameters
    for the inputs. Here, we're storing all the slider inputs, whether the user is a dictator
    or a receiver, and whether they're in the Klee or the Kandinsky group. They're all part of 
    the Player object.
    '''
    level1 = models.IntegerField(widget=widgets.Slider(show_value=False))
    level2 = models.IntegerField(widget=widgets.Slider(show_value=False))
    level3 = models.IntegerField(widget=widgets.Slider(show_value=False))
    level4 = models.IntegerField(widget=widgets.Slider(show_value=False))
    level5 = models.IntegerField(widget=widgets.Slider(show_value=False))
    situation = models.CharField()
    artist_group = models.CharField()
    actual_group_id = models.IntegerField()

    ### Control Questions
    average_question_1 = models.IntegerField(label="Frage 3: Was ist der Durchschnitt von 30 und 40?")
    average_question_2 = models.IntegerField(label="Frage 4: Was ist der Durchschnitt von 37 und 43?")
    percentage_question_1 = models.FloatField(label="Frage 1: Wie viel sind 10% von 65?")
    percentage_question_2 = models.FloatField(label="Frage 2: Wie viel sind 5% von 80?")
    lottery_question_1 = models.IntegerField(label="Wie hoch ist die Wahrscheinlichkeit 40 Punkte zu gewinnen?",
                                             choices=[[70, "70%"], [50, "50%"], [30, "30%"], [10, "10%"]],
                                             widget=widgets.RadioSelect)
    lottery_question_2 = models.BooleanField(
        label="Welche Lotterie sollten Sie auswählen, wenn Sie zwischen diesen beiden Lotterien wählen müssen und dabei die Chance einen höheren Betrag zu gewinnen maximieren sollen",
        choices=[[0, "Lotterie A"], [1, "Lotterie B"]],
        widget=widgets.RadioSelect)


class Subsession(BaseSubsession):
    '''
    Class for the subsession, which is a part of the entire session. The overarching session is made
    up of all the applications. This code is run once for all the players, and the functions are called
    in pages.py. 
    '''

    def making_dictators(self,players):
        '''
        Shuffles all the players, then marks 1/3rd of them as dictators(equally from both the Kandinsky
        and the Klee groups), and the rest of them as receivers.
        '''  
        shuffle(players)                
        total_players = len(players)
        dictators_each_group = int((1/3)*total_players)/2
        klee_dictator_count=kandinsky_dictator_count=dictators_each_group
        for player in players:
            if(player.participant.vars['group']=='Kandinsky' and kandinsky_dictator_count>0):
                player.participant.vars['dictator'] = True            
                kandinsky_dictator_count -= 1
                player.situation = "dictator"
            elif(player.participant.vars['group']=='Klee' and klee_dictator_count>0):
                player.participant.vars['dictator'] = True
                player.situation = "dictator"
                klee_dictator_count -= 1
            else:
                player.participant.vars['dictator'] = False
                player.situation = "receiver"

    def dictator_sequences(self,players):
        '''
        Assigns dictator sequences to all the players, storing the sequences in participant.vars. 
        There are only two sequences possible, which are [2,1] and [1,2], so first two lists are 
        populated with half of [1,2] and half of [2,1] based on the total numbers of players, then
        the list is shuffled and sequences are assigned.
        '''
        players_in_one_group = len(players)//3
        first_group = []
        second_group = []
        dictator_sequences = []
        for _ in range(players_in_one_group):
            first_group.append([1,2])
            first_group.append([2,1])
        receiver_sequences = first_group + second_group
        shuffle(receiver_sequences) #Confirmed with Kavya, shuffling needs to happen
        number_of_dictators = (len(players) - len(receiver_sequences))//2 #We divide by 2 because we're appending two sequences in one iteration

        for _ in range(number_of_dictators):
            dictator_sequences.append([1,2])
            dictator_sequences.append([2,1])
        shuffle(dictator_sequences)

        for player in players:
            if(player.participant.vars['dictator']):
                player.participant.vars['dictator_sequence'] =  dictator_sequences.pop()
            else:
                player.participant.vars['dictator_sequence'] = receiver_sequences.pop(randint(0,len(receiver_sequences)-1))

    def grouping_players(self,players):
        '''
        The main function which takes inputs from all the sliders, sorts the players, and then splits them
        into the Kandinsky and Klee groups.
        '''
        scores = [p.level1 + p.level2 + p.level3 + p.level4 + p.level5 for p in players]  # gets players scores
        sorted_players = [X for _, X in sorted(zip(scores, players), key=lambda pair: pair[0])]
        kandinsky_players = []
        klee_players = []
        # this sorts the players from lowest to highest score
        kandinsky_counter = 1
        klee_counter = 1
        for p in sorted_players[:int(len(sorted_players) / 2)]:
            p.participant.vars['group_member'] = 'Group Member ' + str(kandinsky_counter)
            p.actual_group_id = kandinsky_counter
            kandinsky_counter += 1
            p.participant.vars['group'] = 'Kandinsky'
            p.artist_group = 'Kandinsky'
            kandinsky_players.append(p)
            #print(p, 'variable is', p.participant.vars)
        for p in sorted_players[int(len(sorted_players) / 2):]:
            p.participant.vars['group_member'] = 'Group Member ' + str(klee_counter)
            p.actual_group_id = klee_counter
            klee_counter += 1
            klee_players.append(p)
            p.participant.vars['group'] = 'Klee'
            p.artist_group = 'Klee'


    def match(self,players):
        '''
        Adds some further information in participant.vars for future use. This includes setting player ID that is
        consistent across the entire application, and assigning recievers to all the dictators. This is done by finding
        all the receivers in both the groups first. Then the lists are iterated over and one receiver from each group 
        is assigned to a dictator. Now, since there are two treatments, the same thing is done again, except the iteration
        is reversed in order.
        '''
        reciever_ids = []
        player_id = 1
        blue_id = 0
        red_id = 0
        for player in players:
            player.participant.vars['player_id'] = player_id #Added player id that stays persistent through apps.
            player_id +=1 # Needed for keeping tracks of dictators and receivers.
        kandinsky_receiver_ids = []
        klee_receiver_ids = []
        for player in players:
            player.participant.vars['group_enhancing_payoff'] = []
            player.participant.vars['payoff_array'] = []
            if not player.participant.vars["dictator"]:
                if player.participant.vars["group"] == 'Kandinsky':
                    kandinsky_receiver_ids.append(player.participant.vars['player_id'])
                else:
                    klee_receiver_ids.append(player.participant.vars['player_id'])
            else:
                player.participant.vars['kandinsky_receivers_list'] = []
                player.participant.vars['klee_receivers_list'] = []
                player.participant.vars['active_treatment'] = -1
        shuffle(kandinsky_receiver_ids)
        shuffle(klee_receiver_ids)
        counter = 0
        for player in players:
            if player.participant.vars["dictator"]:
                player.participant.vars['kandinsky_receivers_list'].append(kandinsky_receiver_ids[counter])
                player.participant.vars['klee_receivers_list'].append(klee_receiver_ids[counter])
                counter += 1
        counter = len(kandinsky_receiver_ids)-1
        for player in players:
            if player.participant.vars["dictator"]:
                player.participant.vars['kandinsky_receivers_list'].append(kandinsky_receiver_ids[counter])
                player.participant.vars['klee_receivers_list'].append(klee_receiver_ids[counter])
                counter -= 1