import config
import requests
import json
import os


class WebClient:

    GEOCODE_API_URL = config.GOOGLE_MAPS['geocode_api_url']
    API_KEY = config.GOOGLE_MAPS['api_key']

    def get_address_by_latlong(self, latitude, longitude,):

        url = self.GEOCODE_API_URL

        querystring = {"latlng": latitude+','+longitude,
                       "key": self.API_KEY}

        payload = ""
        headers = {}

        response = requests.request(
            "GET", url, data=payload, headers=headers, params=querystring)
        print("[%s] GET [%s, %s]" % (os.getpid(), url, querystring))
        json_data = json.loads(response.text)
        parsed_address = self.parse_address_from_gmaps(
            json_data, latitude, longitude)

        return parsed_address

    def parse_address_from_gmaps(self, json_data, latitude, longitude):

        # gmaps mock
        # with open('exemplo2.json') as json_file:
        #    data = json.load(json_file)

        # request data
        data = json_data

        # iter results node
        street_number = ''
        road_name = ''
        district_name = ''
        city_name = ''
        state_name = ''
        country_name = ''
        postal_code = ''

        for items in data['results']:

            if ('street_address' in items['types']) or \
               ('sublocality' in items['types']):

                # iter address_componentes node
                for addr_components in items['address_components']:

                    # street number
                    if 'street_number' in addr_components['types']:
                        street_number = addr_components['long_name']

                    # road name
                    if 'route' in addr_components['types']:
                        road_name = addr_components['long_name']

                    # district name
                    if ('sublocality' in addr_components['types']) or\
                            ('sublocality_level_1' in
                             addr_components['types']):

                        district_name = addr_components['long_name']

                    # city name
                    if 'administrative_area_level_2' in\
                       addr_components['types']:

                        city_name = addr_components['long_name']

                    # state name
                    if 'administrative_area_level_1' in\
                       addr_components['types']:

                        state_name = addr_components['long_name']

                    # country name
                    if 'country' in addr_components['types']:
                        country_name = addr_components['long_name']

                    # postal_code
                    if 'postal_code' in addr_components['types']:

                        # no overide postal_code root if exists
                        if postal_code == '':
                            postal_code = addr_components['long_name']

            # parse the postal code if not exists on address_components root
            if ('postal_code' in items['types']) and \
                    not ('postal_code_prefix' in items['types']):

                # iter address_componentes node
                for addr_components in items['address_components']:

                    # postal code
                    if 'postal_code' in addr_components['types']:
                        postal_code = addr_components['long_name']

        parsed_address = {
            "street_number": street_number,
            "road_name": road_name,
            "district_name": district_name,
            "city_name": city_name,
            "state_name": state_name,
            "country_name": country_name,
            "postal_code": postal_code,
            "latitude": latitude,
            "longitude": longitude
        }

        return parsed_address
