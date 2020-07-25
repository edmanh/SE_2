"""
    Generaly used functions and initialisation
    lineno() for printing where something happened
    init_table() to organize an empty database
    get_api_values(<api name>) to get stored api settings from database

    setting up the logger
    checking/generating database
"""

import time
from datetime import datetime
from dateutil import relativedelta
import inspect
import logging
from logging.handlers import RotatingFileHandler

import lib.database as dbtools


def lineno():
    """ -- Create line number --
        Returns the current line number in our program.
        Used for debug reporting debrep()
    """
    return inspect.currentframe().f_back.f_lineno

def set_dpi_awareness():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass

def init_table(se_db, table):
    if table == 'settings':
        selogger.info('Table {} wordt opgebouwd...'.format(table))
        query = """\
CREATE TABLE settings (\
id integer PRIMARY KEY AUTOINCREMENT,\
name text ,\
timeUnit text,\
startDate text,\
endDate text,\
startTime text,\
endTime text\
)"""
        se_db.exec_create(query)  # empty string results in str('NULL')
        records = [('energy', 'DAY', '2020-01-01', '2020-01-31', '', ''),
                   ('timeFrameEnergy', '', '2020-01-01', '2020-01-31', '', ''),
                   ('power', '', '', '', '2020-01-01 06:00:00', '2020-01-01 20:00:00'),
                   ('powerDetails', '', '', '', '2020-01-01 06:00:00', '2020-01-01 20:00:00'),
                   ('energyDetails', 'DAY', '', '', '2020-01-01 06:00:00', '2020-01-01 20:00:00'),
                   ('overview', '', '', '', '', ''),
                   ('details', '', '', '', '', ''),
                   ('dataPeriod', '', '', '', '', ''),
                   ('inventory', '', '', '', '', ''),
                   ('envBenefits', '', '', '', '', '')]
        rows = se_db.exec_executemany('INSERT INTO settings ' +
                                      '(name, timeUnit, startDate, endDate, startTime, endTime) ' +
                                      ' VALUES(?, ?, ?, ?, ?, ?);', records)
        print(f'Tabel {table} build and filled with {rows} rows with default values.')
        return rows


def get_api_values(api_name):
    # Load last used values for api a_name, if available and else all defaults
    a_query = f'SELECT * FROM settings WHERE api_name = "{api_name}"'
    print(f'{__name__}-{lineno()}: query = {a_query}')
    a_names, a_rows = actdb.exec_select(a_query)
    a_row = a_rows[0]  # Result of final query
    arg_db_settings = {}
    for x in range(0, len(a_names)):
        arg_db_settings[a_names[x]] = a_row[x]
    return arg_db_settings

def set_api_value():
    pass


# Set up the rotating logger
selogger = logging.getLogger('selogger')
selogger.setLevel(logging.INFO)
handler = RotatingFileHandler('selog.log', maxBytes=1000, backupCount=0)
selogger.addHandler(handler)
logging.basicConfig(format='%(asctime)s [%(module)s - %(lineno)03d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

# Initiate the database i.e. the 'settings' table
actdb = dbtools.SqliteDb('solaredge.sqlite3', selogger)
numrows = actdb.exec_check_table('settings')
if numrows == 0:
    init_table(actdb, 'settings')


def add_one_month(t):
    """Return a `datetime.date` or `datetime.datetime` (as given) that is
    one month earlier.

    Note that the resultant day of the month might change if the following
    month has fewer days:

        >>> add_one_month(datetime.date(2010, 1, 31))
        datetime.date(2010, 2, 28)
    """
    import datetime
    one_day = datetime.timedelta(days=1)
    one_month_later = t + one_day
    while one_month_later.month == t.month:  # advance to start of next month
        one_month_later += one_day
    target_month = one_month_later.month
    while one_month_later.day < t.day:  # advance to appropriate day
        one_month_later += one_day
        if one_month_later.month != target_month:  # gone too far
            one_month_later -= one_day
            break
    return one_month_later


def check_periode_limit(*x, **y):
    # Must check if d2 > d1 and if d2 - d1 <= delta
    print(f'in check periode **y = {y}')
    val = 1  # default return value, 1 = out of limit
    fmt_t = "%Y-%m-%d %H:%M"  # long date format
    fmt_d = "%Y-%m-%d"  # short date format
    delta = y['delta']
    s_strt = y['strt'][0: 16]  # strip eventual seconds
    s_end = y['end'][0: 16]  # idem
    # print(s_strt, s_end)
    if len(s_strt) > 10:
        d_strt = datetime.strptime(s_strt, fmt_t)
    else:
        d_strt = datetime.strptime(s_strt, fmt_d)
    if len(s_end) > 10:
        d_end = datetime.strptime(s_end, fmt_t)
    else:
        d_end = datetime.strptime(s_end, fmt_d)
    r = relativedelta.relativedelta(d_end, d_strt)
    p_diff = (d_end - d_strt).total_seconds()
    print(f'In periode check: p_diff = {p_diff}')
    if p_diff < 0:
        return -1
    if delta == '':
        return 1        # no periode check needed
    elif delta == 'month':
        if r.years > 1:
            val = 1
        elif r.months == 0:
            val = 0
        elif r.months == 1 & (r.days + r.hours + r.minutes) == 0:
            val = 0
    elif delta == 'year':
        if r.years > 1:
            val = 1
        elif r.years == 0:
            val = 0
        elif r.years == 1 & (r.months + r.days + r.hours + r.minutes) == 0:
            val = 0
        pass
    return val
