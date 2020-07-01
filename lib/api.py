
import requests
from lib.functions import selogger
import lib.config as cnf


class CallApi:
    url_base = None
    api_name = ''

    def __init__(self):
        self.slogger = selogger

    def get_report(self, api_name, url_args):

        site_url = f'https://monitoringapi.solaredge.com/site/{cnf.my_id}/{api_name}'

        response = requests.get(site_url, url_args)
        if not response.status_code == requests.codes.ok:
            print(f'\tEr ging iets mis met deze opdracht, sorry!\n De server gaf errorcode {response.status_code}')
            print(f'De url was: {response.url}')
            print(f'Ontvangen tekst: {response.text}')
            return ''
        return response.text

