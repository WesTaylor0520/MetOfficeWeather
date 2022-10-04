from flask import render_template, request, redirect, url_for, session
from Flask.WeatherApp import app
import main


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        intro = "Please select a location from the list below"

        content = main.getJson()
        locations = main.listOfLocations(content)
        return render_template('home.html', welcome=intro, locations=locations)
    elif request.method == 'POST':
        selectedLocation = request.form['location']
        return redirect(url_for('weatherData', selectedLocation=selectedLocation))


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/weatherData/<selectedLocation>", methods=['GET', 'POST'])
def weatherData(selectedLocation):
    intro = f"3 Hourly Forecasts are shown below for {selectedLocation}:"
    content = main.getJson()
    locations = main.listOfLocations(content)
    selectedLocationId = locations[selectedLocation]
    fiveDayWeatherResults = main.get3HourlyWeather(selectedLocationId)

    return render_template('weatherData.html', title='WeatherData'
                           , welcome=intro
                           , fiveDayWeatherResults=fiveDayWeatherResults)
