CWB_TOKEN = ""
host = "http://127.0.0.1:8080"
server_timezone = 8

BOT_TOKEN = ""
admin = 0

district_to_site = {
    "北投區": "石牌",
    "松山區": "松山",
    "士林區": "士林",
    "內湖區": "內湖",
    "中山區": "臺北",
    "中正區": "臺北",
    "信義區": "信義",
    "大安區": "信義",
    "文山區": "文山",
    "南港區": "松山",
    "大同區": "臺北",
    "萬華區": "臺北",
}

barometer_to_chinese = {
    # reference: https://opendata.cwb.gov.tw/opendatadoc/MFC/ForecastElement.pdf
    # reference: https://opendata.cwb.gov.tw/opendatadoc/DIV2/A0001-001.pdf
    # reference: https://opendata.cwb.gov.tw/opendatadoc/DIV2/A0003-001.pdf
    # now
    "TEMP": "溫度",
    "HUMD": "相對濕度",
    "H_24R": "日累積雨量",
    "24R": "日累積雨量",
    "WDIR": "風向",
    "WDSD": "風速",
    "D_TX": "最高溫",
    "D_TN": "最低溫",
    # forecast
    "PoP12h": "降雨機率",
    "PoP6h": "降雨機率",
    "Wx": "天氣現象",
    "AT": "體感溫度",
    "T": "溫度",
    "RH": "相對濕度",
    "CI": "舒適度",
    "WS": "風速",
    "WD": "風向",
    "Td": "露點溫度",
}
units = {
    # now
    "TEMP": "°C",
    "HUMD": "%",
    "H_24R": "mm",
    "24R": "mm",
    "WDIR": "°",
    "WDSD": "m/s",
    "D_TX": "°C",
    "D_TN": "°C",
    # forecast
    "PoP12h": "%",
    "PoP6h": "%",
    "AT": "°C",
    "T": "°C",
    "RH": "%",
    "CI": "",
    "WS": "m/s",
    "WD": "",
    "Td": "°C",
}
