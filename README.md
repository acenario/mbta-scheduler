# MBTA Commuter Rail Schedule
[![CircleCI](https://circleci.com/gh/acenario/mbta-scheduler.svg?style=svg)](https://circleci.com/gh/acenario/mbta-scheduler)

# Assignment
>The application should show the upcoming departures at North and South stations, the train destinations, the departure times, the track numbers, and the boarding status (e.g. 'Boarding', 'All Aboard', 'Delayed'). The instructions for where to find the real-time data can be found at [mbta.com/developers/v3-api](https://www.mbta.com/developers/v3-api). Obviously, your application does not have to look the same.
Just to give you an idea, this is what the real departure board at North Station looks like:

[![Station](https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/North_Station_departure_board.JPG/800px-North_Station_departure_board.JPG)](https://commons.wikimedia.org/wiki/File:North_Station_departure_board.JPG)

# Django Meets MBTA

MBTA Commuter Rail Schedule is a web application that displays live information for MBTA's Commuter Rail. The application is live at [mbta.arjunb.com](https://mbta.arjunb.com).

### Tech
* [Django] - Secure, fast, and better web development
* [Jinja2] - HTML/CSS + Jinja2 enables nice frontend+backend development
* [jQuery] - jQuery + JS used for frontend polling (future updates will use sockets or event streaming)
* [Materialize] - great UI boilerplate for material UI based web apps

# Features!

  - Live (15s) view of commuter rail departures from both North & South Station
  - Extendable MBTA Class to increase functionality, add more options
  - Secured web application without compromising on CSRF or CORS

### Installation

MBTA Commuter Rail Schedule requires [Python 2] v2.7+ to run. Also requires [pip].

You will also need to replace `MBTA_KEY` in `local_settings.py` to your own MBTA_KEY for the project to run. Keys are available at [api-v3.mbta.com](https://api-v3.mbta.com/).

Install the dependencies and start the server. 


```sh
$ git clone https://github.com/acenario/mbta-scheduler
$ cd mbta-scheduler
$ pip install virtualenv
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ cd CommuterRail
$ mv CommuterRail/local_settings.py.txt CommuterRail/local_settings.py
$ mv CommuterRail/email_info.py.txt CommuterRail/email_info.py
$ python manage.py test
$ python manage.py runserver
```

For production environments... Will share steps using Gunicorn at a later point.

### View the App
You can view the application at [mbta.arjunb.com](https://mbta.arjunb.com) or visit localhost:8000 after running the steps above.

### Todos

 - Convert JS Polling to sockets or event streaming
 - Write more tests
 - Separate North/South into separate pages
 - Support API Versioning in MBTA class

[//]: # (Thanks for reading.)

   [pip]: <https://pip.pypa.io/en/stable/installing/>
   [Python 2]: <https://www.python.org/download/releases/2.7.2/>
   [Materialize]: <https://materializecss.com/>
   [Django]: <https://djangoproject.com>
   [Jinja2]: <https://github.com/pallets/jinja>
   [jQuery]: <https://jquery.com/>
