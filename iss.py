#!/usr/bin/env python

__author__ = 'Kelly Brooks with help from Kathryn'


import turtle
import time
import requests

def people_in_space():
    # Retrieves list of people in space and their craft
    retrieve = requests.get('http://api.open-notify.org/astros.json')
    space = retrieve.json()

    print("Total Astronauts in Space: ", space['number'])

    for person in space["people"]:
        print("Astronaut: {}, Spacecraft: {}".format(
            person["name"],
            person["craft"]
        ))
    
def iss_position():
    # Retrieves location of ISS
    retrieve = requests.get('http://api.open-notify.org/iss-now.json')
    location_of_station = retrieve.json()
    return location_of_station


def time_in_indy():
    # Retrieves flight time of ISS over specific Lat/Long Coordinates
    retrieve = requests.get(
        'http://api.open-notify.org/iss-pass.json?lat=39.768&lon=-86.158')
    flight_time = retrieve.json()
    return time.ctime(flight_time["response"][1]["risetime"])


def space_turtle():
    # Screen displaying the World Map and ISS 
    display = turtle.Screen()
    display.setup(600, 400)
    display.bgpic("./map.gif")
    display.reset()
    display.setworldcoordinates(-180, -90, 180, 90)
    display.addshape("iss.gif")
    display.title("ISS Position Locator")

    # Creates turtle
    turtle.shape("iss.gif")
    turtle.penup()
    turtle.goto(-65, 70)
    turtle.color("green")
    turtle.write(time_in_indy(), font=("Arial", 15, "bold"))
    turtle.goto(float(-86.158), float(39.768))
    turtle.dot(5, 'red')

    while True:
        iss = iss_position()
        position = iss["iss_position"]
        turtle.goto(float(position["longitude"]), float(position["latitude"]))
        time.sleep(10)


def main():
    people_in_space()
    time_in_indy()
    space_turtle()


if __name__ == '__main__':
    main()
