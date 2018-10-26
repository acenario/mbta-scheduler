# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

class RetrieveRoutes(TestCase):
    def setUp(self):
        pass
   
    def test_fetch_endpoint(self):
        """
        This test is meant to highlight if the routes endpoint is working.
        Expected URL to hit: https://api-v3.mbta.com/routes?filter[stop]=South%20Station,place-north&filter[type]=2
        """
        from CommuterRail.settings import MBTA_KEY, MBTA_URL
        import requests

        endpoint = "/routes"
        request_url = MBTA_URL+endpoint
        
        payload = {}
        payload["filter[stop]"] = "South Station,place-north"
        payload["filter[type]"] = "2"
        
        headers = {"x-api-key": MBTA_KEY}

        r = requests.get(
            request_url,
            params=payload,
            headers=headers
        )
        
        self.assertEqual(r.status_code, 200)
    
    def test_fetch_routes_all(self):
        """
        This test is meant to highlight if the routes endpoint is will respond with data.
        Expected URL to hit: https://api-v3.mbta.com/routes?filter[stop]=South%20Station,place-north&filter[type]=2
        """
        import requests
        from CommuterRail.settings import MBTA_KEY, MBTA_URL

        endpoint = "/routes"
        request_url = MBTA_URL+endpoint
        
        payload = {}
        payload["filter[stop]"] = "South Station,place-north"
        payload["filter[type]"] = "2"
        
        headers = {"x-api-key": MBTA_KEY}

        r = requests.get(
            request_url,
            params=payload,
            headers=headers
        )

        routes_response = r.json()

        self.assertIn("data", routes_response)
    
    def test_fetch_routes_north_station(self):
        """
        This test is meant to highlight if the routes endpoint is will respond with data for North Station.
        Expected URL to hit: https://api-v3.mbta.com/routes?filter[stop]=place-north&filter[type]=2
        """
        import requests
        from CommuterRail.settings import MBTA_KEY, MBTA_URL

        endpoint = "/routes"
        request_url = MBTA_URL+endpoint
        
        payload = {}
        payload["filter[stop]"] = "place-north"
        payload["filter[type]"] = "2"
        
        headers = {"x-api-key": MBTA_KEY}

        r = requests.get(
            request_url,
            params=payload,
            headers=headers
        )

        routes_response = r.json()

        self.assertIn("data", routes_response)
    
    def test_fetch_routes_south_station(self):
        """
        This test is meant to highlight if the routes endpoint is will respond with data for South Station.
        Expected URL to hit: https://api-v3.mbta.com/routes?filter[stop]=South Station&filter[type]=2
        """
        import requests
        from CommuterRail.settings import MBTA_KEY, MBTA_URL

        endpoint = "/routes"
        request_url = MBTA_URL+endpoint
        
        payload = {}
        payload["filter[stop]"] = "South Station"
        payload["filter[type]"] = "2"
        
        headers = {"x-api-key": MBTA_KEY}

        r = requests.get(
            request_url,
            params=payload,
            headers=headers
        )

        routes_response = r.json()

        self.assertIn("data", routes_response)

    def test_fetch_routes_north_station_class(self):
        """
        This test is meant to highlight if the routes endpoint is will respond with data for North Station,
        using the MBTA class. The class filters the data for only route ids.
        """
        from CommuterSchedule.mbta import MBTACommuterRail
        from CommuterRail import settings

        MBTA_URL = settings.MBTA_URL
        MBTA_KEY = settings.MBTA_KEY

        mbta = MBTACommuterRail(MBTA_KEY,MBTA_URL)

        routes = mbta.fetch_north_station_routes()

        self.assertGreater(routes, 0)
    
    def test_retrieve_routes_south_station_class(self):
        """
        This test is meant to highlight if the routes endpoint is will respond with data for South Station,
        using the MBTA class. The class filters the data for only route ids.
        """
        from CommuterSchedule.mbta import MBTACommuterRail
        from CommuterRail import settings

        MBTA_URL = settings.MBTA_URL
        MBTA_KEY = settings.MBTA_KEY

        mbta = MBTACommuterRail(MBTA_KEY,MBTA_URL)

        routes = mbta.fetch_south_station_routes()

        self.assertGreater(routes, 0)

    def test_fetch_commuter_rail_departures(self):
        """
        This test is making sure that the dictionary contains the `north_station` and `south_station`
        keys in the dictionary returned
        """
        from CommuterSchedule.mbta import MBTACommuterRail
        from CommuterRail import settings

        MBTA_URL = settings.MBTA_URL
        MBTA_KEY = settings.MBTA_KEY

        mbta = MBTACommuterRail(MBTA_KEY,MBTA_URL)

        departures = mbta.fetch_commuter_rail_departures()

        self.assertIn("north_station", departures)
        self.assertIn("south_station", departures)
