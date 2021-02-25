import unittest
from test_helper import create_app
from flask import url_for
import cases

class ForecastTets(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
    def tearDown(self):
        pass
    def test_correct(self):
        for d in cases.Forecast.correct:
            r = self.client.post(
                url_for("main.forecast"), json={"sitename": d}
            )
            self.assertTrue(r.status_code == 200)
    def test_wrong(self):
        for d in cases.Forecast.wrong:
            r = self.client.post(
                url_for("main.forecast", json={"sitename": d})
            )
            self.assertTrue(r.status_code == 200)