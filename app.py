from flask import Flask, render_template, request
from flask_cors import CORS
from models import *
import requests
import time
import config
import json
from importlib import import_module
import datetime

app = Flask(__name__)
CORS(app)


@app.before_first_request
def fetch_data():
    global data_cache
    data_cache = {
        "forecast_update_time": time.time(),
        "now_update_time": time.time(),
        "forecast": update_forecast(),
        "now": update_now(),
    }


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", weather=None)
    if request.method == "POST":
        site = request.form.get("site")
        weather = json.loads(
            requests.post(
                "%s/api" % config.host, json={"sitename": site, "data_type": "now"}
            ).text
        )
        last_update = datetime.datetime.fromtimestamp(
            data_cache["now_update_time"]
        ).strftime("%Y-%m-%d %H:%M:%S")
        return render_template(
            "index.html",
            site=site,
            weather=weather,
            IMPORT=import_module,
            last_update=last_update,
        )


@app.route("/forecast", methods=["GET", "POST"])
def forecast():
    if request.method == "GET":
        return render_template("forecast.html", weather=None)
    if request.method == "POST":
        site = request.form.get("site")
        weather = json.loads(
            requests.post(
                "%s/api" % config.host, json={"sitename": site, "data_type": "forecast"}
            ).text
        )
        last_update = datetime.datetime.fromtimestamp(
            data_cache["forecast_update_time"] + config.server_timezone * 3600
        ).strftime("%Y-%m-%d %H:%M:%S")
        return render_template(
            "forecast.html",
            weather=weather,
            IMPORT=import_module,
            last_update=last_update,
        )


@app.route("/api", methods=["POST"])
def api():
    payload = request.get_json()
    sitename = payload["sitename"]
    data_type = payload["data_type"]
    if data_type == "forecast":
        if time.time() - data_cache["forecast_update_time"] > 600:
            # update every ten minutes
            data_cache["forecast"] = update_forecast()
        data = data_cache["forecast"]
        for site in data:
            if site["locationName"] == sitename:
                return str(site).replace("'", '"')  # return json
    if data_type == "now":
        if time.time() - data_cache["now_update_time"] > 600:
            data_cache["now"] = update_now()
        data = data_cache["now"]
        return str(data[config.district_to_site[sitename]]).replace("'", '"')


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
