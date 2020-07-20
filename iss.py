#!/usr/bin/env python

__author__ = 'Kelly Brooks with help from Kathryn, Chris and Jackson video from after hours work '


import turtle
import time
import requests

iss_icon = 'iss.gif'
world_map = 'map.gif'
base_url = 'http://api.open-notify.org'

def get_astronaut_info():

    """
    Get a list of the astronatuts currently in space.
    Include their names, the spacecraft that they are
    currently on board, and the total number of
    astronatuts in space.
    """
    r = requests.get(base_url + '/astros.json')
    r.raise_for_status()
    return r.json()['people']


def locate_iss_spacestation():
    """
    Get the current geographic coordinates (lat/lon) of the space station, along with a timestamp.
    Get ISS position (lon, lat) as a float tuple
    """
    r = requests.get(base_url + '/iss-now.json')

    # handles response from server just incase you get anything other than a 200 response
    r.raise_for_status()
    position = r.json()['iss_position']
    lat = float(position['latitude'])
    lon = float(position['longitude'])
    return lat, lon


def map_iss(lat, lon):
    """
    Draw a world map and place ISS icon at lat, lon
    """
    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.bgpic(world_map)
    screen.setworldcoordinates(-180, -90, 180, 90)

    screen.register_shape(iss_icon)
    iss = turtle.Turtle()
    iss.shape(iss_icon)
    iss.setheading(90)
    iss.penup()
    iss.goto(lon, lat)  # note the lon and lat are in reverse order here
    return screen


def compute_rise_time(lat, lon):
    """
    Return the next horizon rise-time of ISS for specific lat/lon
    """
    params = {'lat': lat, 'lon': lon}
    r = requests.get(base_url + '/iss-pass.json', params=params)
    r.raise_for_status()

    passover_time = r.json()['response'][1]['risetime']
    return time.ctime(passover_time)


def main():
    # Part A - get the astronauts and their crafts
    astro_dict = get_astronaut_info()
    print('Current people in space: {}'.format(len(astro_dict)))
    for a in astro_dict:
        print(' - {} in {}'.format(a['name'], a['craft']))

    # Part B - get current position of ISS
    lat, lon = locate_iss_spacestation()
    print('Current ISS coordinates: lat={:.02f} lon={:.02f}'.format(lat, lon))

    # Part C - Render ISS on world map
    screen = None
    try:
        # Attempts to show turtle
        screen = map_iss(lat, lon)

        # Part D - Compute the next pass-over time for Indianapolis, IN
        indy_lat = 39.768403
        indy_lon = -86.158068
        location = turtle.Turtle()
        location.penup()
        location.color('yellow')
        location.goto(indy_lon, indy_lat)
        location.dot(5)
        location.hideturtle()
        next_pass = compute_rise_time(indy_lat, indy_lon)
        location.write(next_pass, align='center', font=('Arial', 12, 'normal'))
    except RuntimeError as e:
        print('ERROR: problem loading graphics: ' + str(e))

    # leave screen open until user clicks on it
    if screen is not None:
        print('Click on screen to exit...')
        screen.exitonclick()


if __name__ == '__main__':
    main()
