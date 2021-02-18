import requests
import json
import config
from os import getenv

CWB_TOKEN = getenv("CWB_TOKEN")


def update_forecast():
    r1 = requests.get(
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-061?"
        "elementName=PoP6h,Wx,AT,T,RH,CI,WS,WD,Td"
        "&Authorization=%s" % CWB_TOKEN
    )
    r2 = requests.get(
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-D0047-069?"
        "elementName=PoP6h,Wx,AT,T,RH,CI,WS,WD,Td"
        "&Authorization=%s" % CWB_TOKEN
    )
    data1 = json.loads(r1.text)["records"]["locations"][0]["location"]
    data2 = json.loads(r2.text)["records"]["locations"][0]["location"]
    return [*data1, *data2]


def update_now():
    # sites list: https://e-service.cwb.gov.tw/wdps/obs/state.htm

    # get data from 自動氣象站(O-A0001-001)
    r1 = requests.get(
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?"
        "Authorization=%s"
        "&locationName=石牌,松山,士林,內湖,大安,文山,新莊,汐止,三重,中和,屈尺"
        "&elementName=TEMP,HUMD,H_24R,WDIR" % CWB_TOKEN
    )
    data1 = dict()
    for site in json.loads(r1.text)["records"]["location"]:
        data1[site["locationName"]] = site["weatherElement"]

    # get data from 局屬氣象站(O-A0003-001)
    r2 = requests.get(
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0003-001?"
        "Authorization=%s"
        "&locationName=臺北,板橋,淡水"
        "&elementName=TEMP,HUMD,24R,WDIR" % CWB_TOKEN
    )
    data2 = dict()
    for site in json.loads(r2.text)["records"]["location"]:
        data2[site["locationName"]] = site["weatherElement"]

    # get 信義 data because there are two sites named '信義'
    r3 = requests.get(
        "https://opendata.cwb.gov.tw/api/v1/rest/datastore/O-A0001-001?"
        "Authorization=%s"
        "&locationName=信義"
        "&elementName=TEMP,HUMD,H_24R,WDIR" % CWB_TOKEN
    )
    site = json.loads(r3.text)["records"]["location"][1]
    data3 = {site["locationName"]: site["weatherElement"]}

    return {**data1, **data2, **data3}
