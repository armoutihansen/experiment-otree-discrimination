from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.1,
    'participation_fee': 4.00,
    'doc': "",
}

SESSION_CONFIGS = [
    {
        'name': 'Jesper_Experiment',
        'display_name': "Dictator Game",
        'num_demo_participants': 6,
        'app_sequence': ['group_creation', 'group_enhancing', 'the_dictator', 'cem', 'final_questionnaire']
    },
    {
        'name': 'Choice_List',
        'display_name': "MPL",
        'num_demo_participants': 1,
        'app_sequence': ['cem']
    },
    {
        'name': 'Contol_Questions',
        'display_name': "Control",
        'num_demo_participants': 1,
        'app_sequence': ['final_questionnaire']
    },
    {
        'name': 'gr_creation',
        'display_name': "gr_creation",
        'num_demo_participants': 6,
        'app_sequence': ['group_creation'],
        'use_browser_bots': False
    },
    {
        'name': 'gr_enhancing',
        'display_name': "gr_enhancing",
        'num_demo_participants': 6,
        'app_sequence': ['group_creation', 'group_enhancing'],
        'use_browser_bots': False
    },
    {
        'name': 'the_dict',
        'display_name': "the_dict",
        'num_demo_participants': 6,
        'app_sequence': ['group_creation', 'group_enhancing', 'the_dictator'],
        'use_browser_bots': False
    },
    {
        'name': 'cem',
        'display_name': "cem",
        'num_demo_participants': 6,
        'app_sequence': ['cem'],
        'use_browser_bots': False
    },
    {
        'name': 'final_questionnaire',
        'display_name': 'final_questionnaire',
        'num_demo_participants': 6,
        'app_sequence': ['final_questionnaire'],
        'use_browser_bots': True
    },
    {
        'name': 'Jesper_Experiment_w_bots',
        'display_name': "Dictator Game with Bots",
        'num_demo_participants': 6,
        'app_sequence': ['group_creation', 'group_enhancing', 'the_dictator', 'cem', 'final_questionnaire'],
        'use_browser_bots': True
    },
]



# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'de'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'EUR'
USE_POINTS = True

ROOMS = [
    {
        'name': 'econ101',
        'display_name': 'Econ 101 class',
        'participant_label_file': '_rooms/econ101.txt',
    },
    {
        'name': 'live_demo',
        'display_name': 'Room for live demo (no participant labels)',
    },
    {
        'name': 'WiSo_lab',
        'display_name': 'WiSo Lab',
        'participant_label_file': '_rooms/wisolab.txt',
    }
]


ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


DEMO_PAGE_INTRO_HTML = """
Here are various games implemented with 
oTree. These games are open
source, and you can modify them as you wish.
"""

# don't share this with anybody.
SECRET_KEY = '3r116b*_uwe#j^+8u@21l1#m93dn@!ir5%!9!ywd89plkvy91d'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'otree_tools']

EXTENSION_APPS = ['otree_tools']

