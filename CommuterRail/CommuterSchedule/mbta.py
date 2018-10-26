import requests
import datetime
import dateutil.parser
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
    
    def fetch_data_from_mbta(self, params,endpoint):
        """General Function to fetch data from MBTA API

        Args:
            params (dict of str: str): Parameters to filter/include 
            endpoint (str): The endpoint requested on the MBTA API
        
        Returns:
            The JSON Dictionary from the MBTA API.

        """

        request_url = self.mbta_url + endpoint
        headers = {"x-api-key": self.mbta_key}

        r = requests.get(
            request_url,
            params=params,
            headers=headers
        )

        return r.json()

    def fetch_north_station_routes(self):
        """Function to fetch commuter routes for North Station
        
        Returns:
            The list of commuter routes in North Station using
            filter[type] = 2.

        """

        endpoint = "/routes"

        payload = {
            "filter[stop]":"place-north",
            "filter[type]": "2"
        }

        routes_response = self.fetch_data_from_mbta(payload,endpoint)
        routes = routes_response["data"]
        
        cleaned_routes = list(route["id"] for route in routes) #Using a generator expression to pull out the commuter routes

        return cleaned_routes

    def create_north_station_payload(self):
        """Function to generate commuter rail predictions
        for North Station
        
        Returns:
            The OrderedDictionary of:
                includes[stop,route,trip]
                filter[route] = All North Station Routes
                filter[stop] = place-north
                filter[direction_id] = 0 || Away trip
                filter[sort] = "departure_time" || Earliest first
        """

        north_station_routes = self.fetch_north_station_routes()
        
        ns_payload = OrderedDict() #Using Ordered Dict to keep track of the sorted list
        ns_payload["include"] = "stop,route,trip"
        ns_payload["filter[stop]"] = "place-north"
        ns_payload["filter[route]"] = ",".join(list(str(route) for route in north_station_routes))
        ns_payload["filter[direction_id]"] = 0
        ns_payload["sort"] = "departure_time"

        return ns_payload


    def fetch_south_station_routes(self):
        """Function to fetch commuter routes for South Station
        
        Returns:
            The list of commuter routes in South Station using
            filter[type] = 2.

        """

        endpoint = "/routes"

        payload = {
            "filter[stop]":"South Station",
            "filter[type]": "2"
        }

        routes_response = self.fetch_data_from_mbta(payload,endpoint)
        routes = routes_response["data"]
        
        cleaned_routes = list(route["id"] for route in routes) #Using a generator expression to pull out the commuter routes

        return cleaned_routes

    def create_south_station_payload(self):
        """Function to generate commuter rail predictions
        for South Station
        
        Returns:
            The OrderedDictionary of:
                includes = stop,route,trip
                filter[route] = All South Station Routes
                filter[stop] = South Station
                filter[direction_id] = 0 || Away trip
                filter[sort] = "departure_time" || Earliest first
        """

        south_station_routes = self.fetch_south_station_routes()
        
        ss_payload = OrderedDict() #Using Ordered Dict to keep track of the sorted list
        ss_payload["include"] = "stop,route,trip"
        ss_payload["filter[stop]"] = "South Station"
        ss_payload["filter[route]"] = ",".join(list(str(route) for route in south_station_routes))
        ss_payload["filter[direction_id]"] = 0
        ss_payload["sort"] = "departure_time"

        return ss_payload

    def fetch_commuter_rail_predictions(self,params):
        """Function to fetch commuter rail predictions
        for a given station payload.

        The Dictionary returned contains each prediction
        organized by keys.

        Args:
            params (dict of str: str): Parameters to filter/include 

        Returns:
            The Dictionary of:
                ROUTE_ID-ISO8601 TIMESTAMP = {
                    prediction_id,
                    departure_time,
                    status,
                    route_id,
                    trip_id,
                    stop_id,
                    headsign,
                    train_number,
                    platform_code
                }
        """
        endpoint = "/predictions"

        predictions_response = self.fetch_data_from_mbta(params,endpoint)
        predictions = predictions_response["data"] #Commuter rail departures
        if not predictions: #Handle those pesky late night commuters wanting that sweet,sweet info
            return None #Sorry, try again in a few hours
        related_data = predictions_response["included"] #Separate relational data from include parameter

        cleaned_predictions = {
            "predictions": OrderedDict(), #Retain sorting in order to keep conssitency 
            "stop": {}, #Using this in order to retrieve platform_code
            "trip": {}, #Using this in order to retrieve headsign data
            "route": {} #Using this to store route ids
        }

        for prediction in predictions:
            prediction_order_id = prediction["relationships"]["route"]["data"]["id"]+"-"+prediction["attributes"]["departure_time"] #Created a unique key for each, could have used prediction_id, however, increased readability 
            departure_time = dateutil.parser.parse(prediction["attributes"]["departure_time"])
            status = prediction["attributes"]["status"]
            if status == "Departed" and departure_time > datetime.datetime.now(self.timezone): #Noticed that API sometimes shows `departed` even though train is late, this helps handle those scenarios
                status = "Delayed"

            cleaned_predictions["predictions"][prediction_order_id] = {
                "prediction_id": prediction["id"],
                "departure_time": departure_time,
                "status": status,
                "route_id": prediction["relationships"]["route"]["data"]["id"],
                "trip_id": prediction["relationships"]["trip"]["data"]["id"],
                "stop_id": prediction["relationships"]["stop"]["data"]["id"],
                "headsign": "",
                "train_number": "",
                "platform_code": "TBD" #This value will be replaced later
            }

            """
            These lines below create a mapping between the prediction 
            and stop,trip,route ids. This helps efficiently lookup the 
            prediction that matches a specific stop,trip, or route id.
            """
            cleaned_predictions["stop"][prediction["relationships"]["stop"]["data"]["id"]] = prediction_order_id
            cleaned_predictions["trip"][prediction["relationships"]["trip"]["data"]["id"]] = prediction_order_id
            cleaned_predictions["route"][prediction["relationships"]["route"]["data"]["id"]] = prediction_order_id

        for related in related_data:
            related_type = related["type"]
            if related_type in cleaned_predictions:
                prediction = cleaned_predictions["predictions"][cleaned_predictions[related_type][related["id"]]] #Lookup based on type happens here, would break if a relation doesn't match a prediction
                if related_type == "stop":
                    if "platform_code" in related["attributes"]:
                        prediction["platform_code"] = related["attributes"]["platform_code"] #Sets the platform_code if available
                elif related_type == "trip":
                    if "headsign" in related["attributes"]:
                        prediction["headsign"] = related["attributes"]["headsign"] #Sets the headsign for the UI
                    else:
                        prediction["headsign"] = "Ended"
                    if "name" in related["attributes"]:
                        prediction["train_number"] = related["attributes"]["name"]

        return cleaned_predictions

    def fetch_north_station_departures(self):
        """Function to fetch commuter rail departures
        for North Station

        The Dictionary returned contains each prediction
        organized by keys.
        
        Returns:
            The Dictionary of:
                ROUTE_ID-ISO8601 TIMESTAMP = {
                    prediction_id,
                    departure_time,
                    status,
                    route_id,
                    trip_id,
                    stop_id,
                    headsign,
                    train_number,
                    platform_code
                }
        """

        return self.fetch_commuter_rail_predictions(self.create_north_station_payload())

    def fetch_south_station_departures(self):
        """Function to fetch commuter rail departures
        for South Station

        The Dictionary returned contains each prediction
        organized by keys.
        
        Returns:
            The Dictionary of:
                ROUTE_ID-ISO8601 TIMESTAMP = {
                    prediction_id,
                    departure_time,
                    status,
                    route_id,
                    trip_id,
                    stop_id,
                    headsign,
                    train_number,
                    platform_code
                }
        """

        return self.fetch_commuter_rail_predictions(self.create_south_station_payload())
    
    def fetch_commuter_rail_departures(self):
        """Function to fetch commuter rail departures
        for both North & South Station

        The Dictionary returned contains each set of
        departures organized by North & South Station.
        
        Returns:
            The Dictionary of:
                north_station = `fetch_north_station_departures()`
                south_station = `fetch_south_station_departures()`
        """

        return {
            "north_station":self.fetch_north_station_departures(),
            "south_station":self.fetch_south_station_departures()
        }

        