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
        idValue = data["Locations"]["Location"][location]["id"]
        locationList[key] = idValue
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
        day = ["Temperature at " + time + " is " + threeHourlyList[i]["Rep"][j]["T"] + "°C",
               "Feels like " + threeHourlyList[i]["Rep"][j]["F"] + "°C",
               "Humidity is " + threeHourlyList[i]["Rep"][j]["H"] + "%",
               "Precipitation probability is " + threeHourlyList[i]["Rep"][j]["Pp"] + "%",
               "Wind Speed is " + threeHourlyList[i]["Rep"][j]["S"] + "mph",
               "Wind Gust is " + threeHourlyList[i]["Rep"][j]["G"] + " mph",
               "Wind Direction is " + threeHourlyList[i]["Rep"][j]["D"]]
        return day

    results = {}
    for i in range(numberOfDays):
        # print("----------------------------------------")

        date = threeHourlyList[i]["value"]
        threeHourlyListReport = threeHourlyList[i]["Rep"]
        numberOfTemperatures = len(threeHourlyListReport)

        key = date[:-1] + "\n"
        values = []

        for j in range(numberOfTemperatures):
            if threeHourlyList[i]["Rep"][j]["$"] == "0":
                values.append(formatConsoleDisplay(midnight))
            elif threeHourlyList[i]["Rep"][j]["$"] == "180":
                values.append(formatConsoleDisplay(threeam))
            elif threeHourlyList[i]["Rep"][j]["$"] == "360":
                values.append(formatConsoleDisplay(sixam))
            elif threeHourlyList[i]["Rep"][j]["$"] == "540":
                values.append(formatConsoleDisplay(nineam))
            elif threeHourlyList[i]["Rep"][j]["$"] == "720":
                values.append(formatConsoleDisplay(midday))
            elif threeHourlyList[i]["Rep"][j]["$"] == "900":
                values.append(formatConsoleDisplay(threepm))
            elif threeHourlyList[i]["Rep"][j]["$"] == "1080":
                values.append(formatConsoleDisplay(sixpm))
            elif threeHourlyList[i]["Rep"][j]["$"] == "1260":
                values.append(formatConsoleDisplay(ninepm))
        results[key] = values

    return results

