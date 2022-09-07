import time

import requests
import requests_cache


# requests_cache.install_cache('demo', backend='sqlite', expire_after=1)


class ApiPowerCuts:

    @staticmethod
    def get_incidents_list():

        # session.cache.clear()
        url = 'https://www.ukpowernetworks.co.uk/api/power-cut/all-incidents'
        result = requests.request("GET", url).json()

        return result

    @staticmethod
    def get_incident_by_id(incident_id):
        url = f'https://www.ukpowernetworks.co.uk/api/power-cut/incident-by-id?id={incident_id}'
        result = requests.request("GET", url)
        return result.json()

    @staticmethod
    def get_fetch_list():
        url = 'https://www.ukpowernetworks.co.uk/api/power-cut/fetch-list'
        result = requests.request("GET", url)
        return result