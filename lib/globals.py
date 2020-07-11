
# global vars for return value of dialog panel
period_start = ''
period_end = ''
period_unit = ''
user_choice = ''
user_val = 0
next_step = ''


title_dict = {}   # api: button titles
help_dict = {}    # api: help_text

rapfilename = ''  # holds name of file to retreive
doccontent = ''   # holds text for gtkText widget

list_of_units_nl = ['Kwartier', 'Uur', 'Dag', 'Week', 'Maand', 'Jaar']
list_of_units_en = ['QUARTER_OF_AN_HOUR', 'HOUR', 'DAY', 'WEEK', 'MONTH', 'YEAR']
hrlist = ['05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22']
mnlist = ['00', '15', '30', '45']



tt = dict()
tt['continue_request'] = 'Hierop klikken betekent\nrapport aanvraag versturen!'
tt['cancel_request'] = 'Hierop klikken betekent\nrapport aanvraag afbreken!'

# ============= Original help info ====================
h_energy = """
Return the site energy measurements.\n
Limited to:\n
 -> one year when using timeUnit=DAY (i.e., daily resolution) and to 
 -> one month when using timeUnit=QUARTER_OF_AN_HOUR or timeUnit=HOUR.\n 
This means that the period between endTime and startTime
should not exceed one year or one month respectively. 
"""

# The next definition is nonsens, result is total anergy and not per time unit!!
h_timeFrameEnergy = """
Return the site total energy produced for a given period.\n
Limited to:
 -> one year when using timeUnit=DAY (i.e., daily resolution).\n
This means that the period between\n
endTime and startTime should not exceed one year).
"""

h_power = """
Return the site power measurements in 15 minutes resolution.\n
Lmited to:\n
 -> A one-month period.\n
This means that the period between\n
endTime and startTime should not exceed one month.
"""

h_powerDetails = """
Detailed site power measurements from meters such as consumption, export (feed-in), import (purchase), etc.
Limited to:\n
 -> A one-month period. 
This means that the period between\n
endTime and startTime should not exceed one month.
"""

h_energyDetails = """
Detailed site energy measurements from meters such as consumption, export (feed-in), import (purchase), etc.\n
Lmited to:\n
 -> A year when using daily resolution (timeUnit=DAY)\n
 -> A month when using hourly resolution of higher (timeUnit=QUARTER_OF_AN_HOUR or timeUnit=HOUR)\n
Lower resolutions (weekly, monthly, yearly) have no period limitation
"""

h_overview = """
Display the site overview data.
"""

h_details = """
Displays the site details, such as name, location, status, etc.
"""

h_dataPeriod = """
Return the energy production start and end dates of the site.
"""

h_inventory = """
Return the inventory of SolarEdge equipment in the site, \n
including inverters/SMIs, batteries, meters, gateways and sensors.
"""

h_envBenefits = """
Returns all environmental benefits based on site energy production: \n
CO 2 emissions saved, equivalent trees planted,\n
and light bulbs powered for a day.
"""

api_help = {
    'energy': h_energy,
    'timeFrameEnergy': h_timeFrameEnergy,
    'power': h_powerDetails,
    'powerDetails': h_powerDetails,
    'energyDetails': h_energyDetails,
    'overview': h_overview,
    'details': h_details,
    'dataPeriod': h_dataPeriod,
    'inventory': h_inventory,
    'envBenefits': h_envBenefits
    }

response_codes = {
    '400': 'The server did not understand the request.',
    '403': 'Forbidden = violation of specific API validation, \nf.e. to many details for given period',
    '429': 'Too many requests',
    }