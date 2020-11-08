import requests
import telebot
import config
class URLTest:
    """
    doc
    """

    def __init__(self, url=None, page="/", BOT_TOKEN=None, SEND_TO=None, test_cases=[], no_data_test=True, auto_send_result=True):
        self.url = url
        self.page = page
        self.BOT_TOKEN = BOT_TOKEN
        self.bot = telebot.TeleBot(self.BOT_TOKEN)
        self.SEND_TO = SEND_TO
        self.test_cases = test_cases
        self.results = []
        self.no_data_test = no_data_test
        self.auto_send_result = auto_send_result

    def run_test(self):
        if self.no_data_test:
            r = requests.get(self.url + self.page)
            result = '%s: %s\ntake `%s` seconds'%(r.request.method, r.status_code, r.elapsed.total_seconds())
            self.results.append(result)
        for test in self.test_cases:
            print(self.url + self.page, test)
            r = requests.post(self.url + self.page, data=test)
            result = '%s `%s`: %s\ntake `%s` seconds'%(r.request.method, str(test), r.status_code, r.elapsed.total_seconds())
            self.results.append(result)

        self.bot.send_message(self.SEND_TO, '*Service Self Test: \n%s\n\n*'%(self.url + self.page) + '\n'.join(self.results), parse_mode='Markdown')


def run_test():
    test_cases = [
        {"site": "北投區"},
        {"site": "士林區"},
        {"site": "大同區"},
        {"site": "中山區"},
        {"site": "松山區"},
        {"site": "內湖區"},
        {"site": "萬華區"},
        {"site": "中正區"},
        {"site": "大安區"},
        {"site": "信義區"},
        {"site": "南港區"},
        {"site": "文山區"},
    ]
    '''
    test_cases_api = [
        {"sitename": "北投區", "data_type": "now"}
    ]
    '''
    
    index_test = URLTest(
        url=config.host,
        page="/",
        BOT_TOKEN=config.BOT_TOKEN,
        SEND_TO=config.admin,
        test_cases=test_cases,
        no_data_test=True,
    )
    index_test.run_test()
    
    forecast_test = URLTest(
        url=config.host,
        page="/forecast",
        BOT_TOKEN=config.BOT_TOKEN,
        SEND_TO=config.admin,
        test_cases=test_cases,
        no_data_test=True,
    )
    forecast_test.run_test()
    '''
    api_test = URLTest(
        url=config.host,
        page="/api",
        BOT_TOKEN=config.BOT_TOKEN,
        SEND_TO=config.admin,
        test_cases=test_cases_api,
        no_data_test=False,
    )
    api_test.run_test()
    '''