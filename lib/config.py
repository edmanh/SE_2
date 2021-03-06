"""


"""
from os import getcwd
import sys

sys.path.insert(0, 'D:\\CloudStation\\Developments\\SolarEdge')  # Location of private files
from private import PrivateValues as PV                          # not recognised by PyCharm !!

project_alive = True    # If project not alive calls to web site will be skipped
wfquit = 5000           # Wait for quit == automatic close message pop-up

# Private fixed api arguments stored in location outside project
my_key = PV.my_key
my_id = PV.my_id

# System settings
report_dir = '..\\SolarEdge\\reports\\'  # Without a preceding '\', this is appended to the program dir.
tmp_file = 'new_report.txt'

# My standard fonts
fa12 = ('Arial', 12)
fh16 = ('Helvetica', 16)
fh14 = ('Helvetica', 14)
fh13 = ('Helvetica', 13)
fh12 = ('Helvetica', 12)
fh11 = ('Helvetica', 11)

api_config = {  # Translation and arguments to provide for a particular api
    'energy': {'args':           # OK - Production between dates and in Wh per timeUnit
                ['Periodeopbrengst in detail', 'startDate', 'endDate', 'timeUnit'],
                'info': 'Opbrengst per ingegeven periode maar met een beperkte lengte!:\n'
                        'max. 1 jaar bij een interval van één dag,\n'
                        'max. 1 maand bij een interval kleiner dan een dag.'},
    'timeFrameEnergy': {'args':  # OK - Energy summary over given period
                ['Periodeopbrengst samenvatting', 'startDate', 'endDate'],
                'info': 'Geeft de totale energieproductie over de gewenste periode.'},
    'power': {'args':            # OK - Energy per 15 min, max 1 month
                ['Periodeopbrengst per kwartier', 'startTime', 'endTime'],
                'info': 'Opbrengst per kwartier over max. één maand.\n'},
    'overview': {'args':         # no arguments, OK - High lites until today with details
                ['Overzicht'], 'info': 'Samenvattingen van opbrengst per typische periodes zoals:\n'
                                       'Gehele periode, laatste jaar, laatste maand etc.\n'
                                       'Er zijn geen andere informaties nodig.'},
    'details': {'args':          # OK - Installation details
                ['Installatiedetails'], 'info': 'Allerlei details over het account en de installatie.\n'
                                                'Er zijn geen andere informaties nodig.'},
    'dataPeriod': {'args':       # OK - Just start- and enddate of installation.
                ['Actuele looptijd'], 'info': 'Dit rapport biedt alleen de begin- en actuele datum.\n'
                                              'Er zijn geen andere informaties nodig.'},
    'inventory': {'args':        # OK - List of technical installation details
                ['Technische details'], 'info': 'Geeft een lijst(je) met apparatuurdetails.\n'
                                                'Er zijn geen andere informaties nodig.'},
    'envBenefits': {'args':      # OK - Environment benefits like CO2
                ['Millieuvoordeel'], 'info': 'Zoals de naam aangeeft worden gerealiseerde (berekende) millieuvoordelen gepresenteerd.\n'
                                             'Er zijn geen andere informaties nodig.'},
    }

# Set up app indices for translated choices and help balloons

all_titles = dict()   # Holds button titles
all_args = dict()     # Holds api args
all_info = dict()     # Holds api info
for app, attribs in api_config.items():
    all_args[app] = attribs['args']
    all_info[app] = attribs['info']
    all_titles[app] = attribs['args'][0]  # App Button Titles


'''
query = 'SELECT name, help_text from helptext'
names, help_records = func.actdb.exec_select(query)
for record in help_records:
    gl.help_dict[record[0]] = record[1]
'''
