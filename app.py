from flask import Blueprint, request, url_for, render_template, Flask
from flask_cors import CORS
from models import update_forecast, update_now
import time
import json
from conversion_table import district_to_site, barometer_to_chinese, units
from importlib import import_module
import datetime
from os import getenv
import config
import requests


app = Flask(__name__)
app.config.from_object(config.config_list[getenv("env")])
main = Blueprint("main", __name__)
CORS(app)

timezone = int(getenv("timezone"))


@main.before_app_first_request
def init():
    global data_cache
    data_cache = {
        "forecast_update_time": time.time(),
        "now_update_time": time.time(),
        "forecast": update_forecast(),
        "now": update_now(),
    }


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", weather=None)
    if request.method == "POST":
        sitename = request.form.get("site")
        if time.time() - data_cache["now_update_time"] > 600:
            data_cache["now"] = update_now()
            data_cache["now_update_time"] = time.time()
        weather = data_cache["now"].get(district_to_site.get(sitename, None), None)
        last_update = datetime.datetime.fromtimestamp(
            data_cache["now_update_time"] + timezone * 3600
        ).strftime("%Y-%m-%d %H:%M:%S")
        return render_template(
            "index.html",
            site=sitename,
            weather=weather,
            IMPORT=import_module,
            last_update=last_update,
        )


@main.route("/forecast", methods=["GET", "POST"])
def forecast():
    if request.method == "GET":
        return render_template("forecast.html", weather=None)
    if request.method == "POST":
        sitename = request.form.get("site")
        if time.time() - data_cache["forecast_update_time"] > 600:
            data_cache["forecast"] = update_forecast()
            data_cache["forecast_update_time"] = time.time()
        data = data_cache["forecast"]
        weather = None
        for site in data:
            print(site["locationName"])
            if site["locationName"] == sitename:
                weather = site
        last_update = datetime.datetime.fromtimestamp(
            data_cache["forecast_update_time"] + timezone * 3600
        ).strftime("%Y-%m-%d %H:%M:%S")
        return render_template(
            "forecast.html",
            weather=weather,
            IMPORT=import_module,
            last_update=last_update,
        )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
