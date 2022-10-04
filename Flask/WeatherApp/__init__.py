from flask import Flask

app = Flask(__name__)

from Flask.WeatherApp import routes
