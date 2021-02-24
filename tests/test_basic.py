import unittest
from test_helper import create_app
from flask import url_for
import cases


class BasicTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

    def tearDown(self):
        pass
    
    def test_now_alive(self):
        r = self.client.get(url_for("main.index"))
        self.assertTrue(r.status_code == 200)
        
    def test_forecast_alive(self):
        r = self.client.get(url_for("main.forecast"))
        self.assertTrue(r.status_code == 200)
        
    def test_404(self):
        r = self.client.get("nothis")
        self.assertTrue(r.status_code == 404)
