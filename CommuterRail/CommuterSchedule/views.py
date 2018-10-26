import requests
from django.shortcuts import render
from django.http.response import HttpResponse


def makerequest():
    url = ""
    #GET ROUTES FIRST: https://api-v3.mbta.com/routes?filter[stop]=South%20Station&filter[type]=2
    #GET ROUTES SECOND: https://api-v3.mbta.com/routes?filter[stop]=place-north&filter[type]=2


def index(request):
    """
    View function for home page of site.
    """

    current_page = 'home'
    return render(request, 
                  "index.html", 
                  locals(), 
                  )