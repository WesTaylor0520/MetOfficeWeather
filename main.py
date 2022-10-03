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

    for i in range(numberOfDays):
        print("----------------------------------------")
        date = threeHourlyList[i]["value"]
        print(date[:-1])
        threeHourlyListReport = threeHourlyList[i]["Rep"]
        numberOfTemperatures = len(threeHourlyListReport)
        for j in range(numberOfTemperatures):
            print("Temperature " + threeHourlyList[i]["Rep"][j]["T"])
            print("Feels like " + threeHourlyList[i]["Rep"][j]["F"] + "\n")


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
