"""


"""
from os import getcwd
import lib.globals as gl
import lib.functions as func


# If project not alive calls to web site will be skipped
project_alive = True  # False
testing = True
wait_for_quit = 5000

# Private fixed api arguments
my_key = 'RMLUX25VINZSEWLYKCIR5L6KJMFESHM8'
my_id = '1123532'

# System settings
report_dir = 'reports\\'  # Without a preceding '\', this is appended to the program dir.
myhome = getcwd()
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
                'info': 'Opbrengst per ingegeven periode maar met een beperkte lengte:\n'
                        '1 maand bij een interval kleiner dan dan een dag,\n'
                        '1 jaar bij een interval kleiner dan een maand'},
    'timeFrameEnergy': {'args':  # OK - Energy summary over given period
                ['Periodeopbrengst samenvatting', 'startDate', 'endDate'],
                'info': 'Info tekst'},
    'power': {'args':            # OK - Energy per 15 min, max 1 month
                ['Periodeopbrengst per kwartier', 'startTime', 'endTime'],
                'info': 'Opbrengst per kwartier over max. één maand.\n'},
    'powerDetails': {'args':     # OK - 15min resolution from misc. meters
                ['Diverse energiedetails 15min.', 'startTime', 'endTime'],
                'info': 'Info tekst'},
    'energyDetails': {'args':    # Like powerDetails but own time interval
                ['Opbrengst met interval keuze', 'startTime', 'endTime', 'timeUnit'],
                'info': 'Info tekst'},
    'overview': {'args':         # no arguments, OK - High lites until today with details
                ['Overzicht'], 'info': 'No arguments'},
    'details': {'args':          # OK - Installation details
                ['Installatiedetails'], 'info': 'No arguments'},
    'dataPeriod': {'args':       # OK - Just start- and enddate of installation.
                ['Actuele looptijd'], 'info': 'No arguments'},
    'inventory': {'args':        # OK - List of technical installation details
                ['Technische details'], 'info': 'No arguments'},
    'envBenefits': {'args':      # OK - Environment benefits like CO2
                ['Millieuvoordeel'], 'info': 'No arguments'},
    }

# Set up app indices for translated choices and help balloons
query = 'SELECT api_name, help_text from helptext'
names, help_records = func.actdb.exec_select(query)
for record in help_records:
    gl.help_dict[record[0]] = record[1]
all_titles = {}     # Holds button titles
all_args = dict()   # Holds api args
all_info = dict()   # Holds api info
for app, attribs in api_config.items():
    all_args[app] = attribs['args']
    all_info[app] = attribs['info']
    all_titles[app] = attribs['args'][0]  # App Button Titles

