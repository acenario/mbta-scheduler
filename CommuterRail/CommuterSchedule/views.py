import json
import requests
import datetime
from django.conf import settings
from django.shortcuts import render
from django.http.response import HttpResponse
from CommuterSchedule.mbta import MBTACommuterRail

def index(request):
    """
    View function for home page of site.
    """

    MBTA_URL = settings.MBTA_URL
    MBTA_KEY = settings.MBTA_KEY

    mbta = MBTACommuterRail(MBTA_KEY,MBTA_URL)

    departures = mbta.fetch_commuter_rail_departures()
    
    north_station = departures["north_station"]
    if north_station:
        north_station = departures["north_station"]["predictions"]

    south_station = departures["south_station"]
    if south_station:
        south_station = departures["south_station"]["predictions"]

    now = datetime.datetime.now()
    today = now.strftime("%A")
    date = now.strftime("%Y-%-m-%-d")
    time = now.strftime("%-I:%M %p")

    current_page = 'home'

    return render(request, 
                  "index.html", 
                  locals(), 
                  )

def get_page_info(request):
    """
    This API endpoint allows for a simple polling solutions
    Normally, would opt for sockets or MBTA's event streaming
    but for a simple project, this solution works
    """
    if request.is_ajax():
        if request.method == 'POST':
            MBTA_URL = settings.MBTA_URL
            MBTA_KEY = settings.MBTA_KEY

            mbta = MBTACommuterRail(MBTA_KEY,MBTA_URL)

            departures = mbta.fetch_commuter_rail_departures()

            north_station = departures["north_station"]
            if north_station:
                north_station = departures["north_station"]["predictions"]

                for key,value in north_station.items():
                    value["departure_time"] = value["departure_time"].strftime("%-I:%M %p").replace("AM","a.m.").replace("PM", "p.m.")
                
            south_station = departures["south_station"]
            if south_station:
                south_station = departures["south_station"]["predictions"]

                for key,value in south_station.items():
                    value["departure_time"] = value["departure_time"].strftime("%-I:%M %p").replace("AM","a.m.").replace("PM", "p.m.")
            
            now = datetime.datetime.now()
            today = now.strftime("%A")
            date = now.strftime("%Y-%-m-%-d")
            time = now.strftime("%-I:%M %p")
            
            return HttpResponse(
                json.dumps(
                    {
                        "north_station": north_station,
                        "south_station": south_station,
                        "today": today,
                        "date": date,
                        "time": time
                    }
                ), content_type="application/json"
            )
    
    return HttpResponse(
                {
                    "error": "Invalid Request",
                }, content_type="application/json"
            )

