import requests
import json
import config


def update_data():
    r = requests.get(
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-061?Authorization=%s"%config.CWB_TOKEN
    )
    data = json.loads(r.text)
    return data
