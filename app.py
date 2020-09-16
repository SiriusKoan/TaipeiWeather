from flask import Flask, render_template, request
from flask_cors import CORS
from models import *
import requests
import time
import config
import json

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", site=None)
    if request.method == "POST":
        site = request.form.get("site")
        weather = json.loads(requests.post('%s/api'%config.host, json = {'sitename': site}).text)
        return render_template("index.html", weather=weather, time=[weather['weatherElement'][0]['time'][0]['startTime'], weather['weatherElement'][0]['time'][-1]['endTime']])


@app.route("/api", methods=["POST"])
def api():
    payload = request.get_json()
    sitename = payload['sitename']
    if time.time() - data_cache['update_time'] > 3600:
        # update every one hour
        data_cache['data'] = update_data()
    data = data_cache['data']['records']['locations'][0]['location']
    for site in data:
        if site['locationName'] == sitename:
            return str(site).replace('\'', '\"')



if __name__ == "__main__":
    data_cache = {'update_time': time.time() ,'data': update_data()}
    app.run(host="127.0.0.1", port=8080, debug=True)
