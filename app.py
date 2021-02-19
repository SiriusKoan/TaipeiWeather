from flask import render_template, request, abort
from models import create_app, update_forecast, update_now
import time
from conversion_table import district_to_site, barometer_to_chinese, units
import json
from importlib import import_module
import datetime
import config
from os import getenv

app = create_app('TaipeiWeather', config.config_list[getenv('env')])
host = getenv("host")
timezone = int(getenv("timezone"))
self_request = app.test_client()

@app.before_first_request
def init():
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
        weather = self_request.post("/api", json={"sitename": site, "data_type": "now"}).get_json(force=True)
        last_update = datetime.datetime.fromtimestamp(
            data_cache["now_update_time"] + timezone * 3600
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
        weather = self_request.post("/api", json={"sitename": site, "data_type": "forecast"}).get_json(force=True)
        last_update = datetime.datetime.fromtimestamp(
            data_cache["forecast_update_time"] + timezone * 3600
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
        return ''
    if data_type == "now":
        if time.time() - data_cache["now_update_time"] > 600:
            data_cache["now"] = update_now()
        data = data_cache["now"]
        return str(data.get(district_to_site[sitename], '')).replace("'", '"')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
