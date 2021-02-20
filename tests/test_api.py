import unittest
from test_helper import create_app
from flask import current_app, url_for
import cases


class APITest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def get_json(self, r):
        try:
            data = r.get_json(force=True)
            return True
        except:
            return False

    def test_now_correct(self):
        for d in cases.Now.correct:
            r = self.client.post(
                url_for("main.api"), json={"sitename": d, "data_type": "now"}
            )
            self.assertTrue(r.status_code == 200)
            self.assertTrue(self.get_json(r))

    def test_now_wrong(self):
        for d in cases.Now.wrong:
            r = self.client.post(
                url_for("main.api"), json={"sitename": d, "data_type": "now"}
            )
            self.assertTrue(r.status_code == 200)
            self.assertFalse(self.get_json(r))

    def test_forecast_correct(self):
        for d in cases.Forecast.correct:
            r = self.client.post(
                url_for("main.api"), json={"sitename": d, "data_type": "forecast"}
            )
            self.assertTrue(r.status_code == 200)
            self.assertTrue(self.get_json(r))

    def test_forecast_wrong(self):
        for d in cases.Forecast.wrong:
            r = self.client.post(
                url_for("main.api", json={"sitename": d, "data_type": "forecast"})
            )
            self.assertTrue(r.status_code == 200)
            self.assertFalse(self.get_json(r))
