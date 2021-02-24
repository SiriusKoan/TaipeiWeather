import unittest
from test_helper import create_app
from flask import url_for
import cases


class NowTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

    def tearDown(self):
        pass
    
    def test_correct(self):
        for d in cases.Now.correct:
            r = self.client.post(
                url_for("main.index"), json={"sitename": d, "data_type": "now"}
            )
            self.assertTrue(r.status_code == 200)

    def test_wrong(self):
        for d in cases.Now.wrong:
            r = self.client.post(
                url_for("main.index"), json={"sitename": d, "data_type": "now"}
            )
            self.assertTrue(r.status_code == 200)