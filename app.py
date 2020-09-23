from flask import Flask, render_template, request
from flask_cors import CORS
from models import *
import requests
import time
import config
import json

app = Flask(__name__)
CORS(app)

@app.before_first_request
def fetch_data():
    global data_cache
    data_cache = {'forecast_update_time': time.time(), 'now_update_time': time.time() ,'forecast': update_forecast(), 'now': update_now()}


@app.route("/", methods=["GET"])
def index():
    if request.args.get('site'):
        site = request.args.get("site")
        weather = json.loads(requests.post('%s/api'%config.host, json={'sitename': site, 'data_type': 'now'}).text)
        return render_template("index.html", weather=weather)
    else:
        return render_template("index.html", site=None)
        


@app.route("/forecast", methods=["GET", "POST"])
def forecast():
    if request.method == "GET":
        return render_template("forecast.html", site=None)
    if request.method == "POST":
        site = request.form.get("site")
        weather = json.loads(requests.post('%s/api'%config.host, json = {'sitename': site, 'data_type': 'forecast'}).text)
        return render_template("forecast.html", weather=weather, time=[weather['weatherElement'][0]['time'][0]['startTime'], weather['weatherElement'][0]['time'][-1]['endTime']])


@app.route("/api", methods=["POST"])
def api():
    payload = request.get_json()
    sitename = payload['sitename']
    data_type = payload['data_type']
    if data_type == 'forecast':
        if time.time() - data_cache['forecast_update_time'] > 3600:
            # update every one hour
            data_cache['forecast'] = update_forecast()
        data = data_cache['forecast']
        for site in data:
            if site['locationName'] == sitename:
                return str(site).replace('\'', '\"') # return json
    if data_type == 'now':
        if time.time() - data_cache['now_update_time'] > 3600:
            data_cache['now'] = update_now()
        data = data_cache['now']
        return str(data[config.district_to_site[sitename]]).replace('\'', '\"')



if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
