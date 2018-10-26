import requests
from CommuterSchedule.utils import UTC

class MBTACommuterRail(object):
    """MBTA Class with supported functions to get stuff"""

    def __init__(self,mbta_key,mbta_url):
        self.timezone = UTC()
        self.mbta_key = mbta_key
        self.mbta_url = mbta_url

    def fetch_data_from_mbta(self, payload,endpoint):
        request_url = self.mbta_url + endpoint
        headers = {"x-api-key": self.mbta_key}

        r = requests.get(
            request_url,
            params=payload,
            headers=headers
        )

        return r.json()

    def fetch_north_station_routes(self):
        endpoint = "/routes"

        payload = {
            "filter[stop]":"place-north",
            "filter[type]": "2"
        }

        routes_response = self.fetch_data_from_mbta(payload,endpoint)
        routes = routes_response["data"]
        
        cleaned_routes = list(route["id"] for route in routes)

        return cleaned_routes

    def fetch_south_station_routes(self):
        endpoint = "/routes"

        payload = {
            "filter[stop]":"South Station",
            "filter[type]": "2"
        }

        routes_response = self.fetch_data_from_mbta(payload,endpoint)
        routes = routes_response["data"]
        
        cleaned_routes = list(route["id"] for route in routes)

        return cleaned_routes
        