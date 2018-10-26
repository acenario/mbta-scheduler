import requests
from django.shortcuts import render
from django.http.response import HttpResponse
from CommuterSchedule.mbta import MBTACommuterRail

def index(request):
    """
    View function for home page of site.
    """

    current_page = 'home'
    return render(request, 
                  "index.html", 
                  locals(), 
                  )