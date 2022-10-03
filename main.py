import requests
import json
from api_key import API_KEY

SITELIST_URL = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/sitelist?key="
THREEHOURLY_URL_1 = "http://datapoint.metoffice.gov.uk/public/data/val/wxfcs/all/json/"
THREEHOURLY_URL_2 = "?res=3hourly&key="


def getValuesAtDeepestLayer(my_dict):
    sub_vals = []
    actual_vals = []
    for val in my_dict.values():
        try:
            sub_vals += getValuesAtDeepestLayer(val)
        except AttributeError:
            actual_vals += [val]

    return sub_vals + actual_vals


def getJson():
    content = requests.get(SITELIST_URL + API_KEY)
    parsedJson = json.loads(content.text)
    return parsedJson


def listOfLocations(data):
    listDeepestLayer = getValuesAtDeepestLayer(data)
    numberOfLocations = len(listDeepestLayer[0])
    locationList = {}
    for location in range(numberOfLocations):
        key = data["Locations"]["Location"][location]["name"]
        value = data["Locations"]["Location"][location]["id"]
        locationList[key] = value
        print(data["Locations"]["Location"][location]["name"])
    return locationList


def get3HourlyWeather(location):
    weatherData = requests.get(THREEHOURLY_URL_1 + location + THREEHOURLY_URL_2 + API_KEY)
    weatherJSON = json.loads(weatherData.text)
    threeHourlyList = weatherJSON["SiteRep"]["DV"]["Location"]["Period"]
    numberOfDays = len(threeHourlyList)

    midnight = "00:00"
    threeam = "03:00"
    sixam = "06:00"
    nineam = "09:00"
    midday = "12:00"
    threepm = "15:00"
    sixpm = "18:00"
    ninepm = "21:00"

    def formatConsoleDisplay(time):
        print("Temperature at " + time + " is " + threeHourlyList[i]["Rep"][j]["T"] + "°C")
        print("Feels like " + threeHourlyList[i]["Rep"][j]["F"] + "°C")
        print("Humidity is " + threeHourlyList[i]["Rep"][j]["H"] + "%")
        print("Precipitation probability is " + threeHourlyList[i]["Rep"][j]["Pp"] + "%")
        print("Wind Speed is " + threeHourlyList[i]["Rep"][j]["S"] + "mph")
        print("Wind Gust is " + threeHourlyList[i]["Rep"][j]["G"] + " mph")
        print("Wind Direction is " + threeHourlyList[i]["Rep"][j]["D"] + "\n")

    for i in range(numberOfDays):
        print("----------------------------------------")
        date = threeHourlyList[i]["value"]
        print(date[:-1] + "\n")
        threeHourlyListReport = threeHourlyList[i]["Rep"]
        numberOfTemperatures = len(threeHourlyListReport)
        for j in range(numberOfTemperatures):
            if threeHourlyList[i]["Rep"][j]["$"] == "0":
                formatConsoleDisplay(midnight)
            elif threeHourlyList[i]["Rep"][j]["$"] == "180":
                formatConsoleDisplay(threeam)
            elif threeHourlyList[i]["Rep"][j]["$"] == "360":
                formatConsoleDisplay(sixam)
            elif threeHourlyList[i]["Rep"][j]["$"] == "540":
                formatConsoleDisplay(nineam)
            elif threeHourlyList[i]["Rep"][j]["$"] == "720":
                formatConsoleDisplay(midday)
            elif threeHourlyList[i]["Rep"][j]["$"] == "900":
                formatConsoleDisplay(threepm)
            elif threeHourlyList[i]["Rep"][j]["$"] == "1080":
                formatConsoleDisplay(sixpm)
            elif threeHourlyList[i]["Rep"][j]["$"] == "1260":
                formatConsoleDisplay(ninepm)


def main():
    print("Hello, Welcome to the program \n"
          "A list of available locations will be shown below \n")

    content = getJson()
    locations = listOfLocations(content)

    locationChoice = input("\nPlease select a location from the list: \n")
    if locationChoice in locations:
        print(f"Displaying weather forecast for {locationChoice}")
        get3HourlyWeather(locations[locationChoice])


if __name__ == '__main__':
    main()
