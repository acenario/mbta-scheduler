import requests
import dateutil.parser
from datetime import datetime
from CommuterSchedule.utils import UTC
from collections import OrderedDict

class MBTACommuterRail(object):
    """MBTA Class that currently fetches real-time Commuter Rail Departures
    
    Currently this class supports commuter rail departures for North & South Station.
    Additonally functionality, stations, and support can be added. 

    Args:
        mbta_key (str): This is the developer key provided by MBTA
        mbta_url (str): This is the current url for the MBTA API

    TODO:
        * Support versioning

    """

    def __init__(self,mbta_key,mbta_url):
        self.timezone = UTC()
        self.mbta_key = mbta_key
        self.mbta_url = mbta_url

        if mbta_url != "https://api-v3.mbta.com":
            raise Exception("The Project doesn't currently support different versions of the API. It only supports v3 with this url: {}".format("https://api-v3.mbta.com"))

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

    def create_north_station_payload(self):
        north_station_routes = self.fetch_north_station_routes()
        
        ns_payload = OrderedDict()
        ns_payload["include"] = "stop,route,trip"
        ns_payload["filter[stop]"] = "place-north"
        ns_payload["filter[route]"] = ",".join(list(str(route) for route in north_station_routes))
        ns_payload["filter[direction_id]"] = 0
        ns_payload["sort"] = "departure_time"

        return ns_payload


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

    def create_south_station_payload(self):
        south_station_routes = self.fetch_south_station_routes()
        
        ss_payload = OrderedDict()
        ss_payload["include"] = "stop,route,trip"
        ss_payload["filter[stop]"] = "South Station"
        ss_payload["filter[route]"] = ",".join(list(str(route) for route in south_station_routes))
        ss_payload["filter[direction_id]"] = 0
        ss_payload["sort"] = "departure_time"

        return ss_payload

    def fetch_commuter_rail_predictions(self,params):
        endpoint = "/predictions"

        predictions_response = self.fetch_data_from_mbta(params,endpoint)
        predictions = predictions_response["data"]
        related_data = predictions_response["included"]

        cleaned_predictions = {
            "predictions": OrderedDict(),
            "stop": {},
            "trip": {},
            "route": {}
        }

        for prediction in predictions:
            prediction_order_id = prediction["relationships"]["route"]["data"]["id"]+"-"+prediction["attributes"]["departure_time"]
            departure_time = dateutil.parser.parse(prediction["attributes"]["departure_time"])
            status = prediction["attributes"]["status"]
            if status == "Departed" and departure_time > datetime.now(self.timezone):
                status = "Delayed"

            cleaned_predictions["predictions"][prediction_order_id] = {
                "prediction_id": prediction["id"],
                    "departure_time": departure_time,
                    "status": status,
                    "route_id": prediction["relationships"]["route"]["data"]["id"],
                    "trip_id": prediction["relationships"]["trip"]["data"]["id"],
                    "stop_id": prediction["relationships"]["stop"]["data"]["id"],
                    "platform_code": "TBD"
            }
            cleaned_predictions["stop"][prediction["relationships"]["stop"]["data"]["id"]] = prediction_order_id
            cleaned_predictions["trip"][prediction["relationships"]["trip"]["data"]["id"]] = prediction_order_id
            cleaned_predictions["route"][prediction["relationships"]["route"]["data"]["id"]] = prediction_order_id

        for related in related_data:
            related_type = related["type"]
            if related_type in cleaned_predictions:
                prediction = cleaned_predictions["predictions"][cleaned_predictions[related_type][related["id"]]]
                if related_type == "stop":
                    if "platform_code" in related["attributes"]:
                        prediction["platform_code"] = related["attributes"]["platform_code"]
                elif related_type == "trip":
                    if "headsign" in related["attributes"]:
                        prediction["headsign"] = related["attributes"]["headsign"]
                    else:
                        prediction["headsign"] = "Ended"

        return cleaned_predictions

    def fetch_north_station_departures(self):
        return self.fetch_commuter_rail_predictions(self.create_north_station_payload)

    def fetch_south_station_departures(self):
        return self.fetch_commuter_rail_predictions(self.create_south_station_payload)
    
    def fetch_commuter_rail_schedule(self):
        return {
            "north_station":self.fetch_north_station_departures(),
            "south_station":self.fetch_south_station_departures()
        }

        