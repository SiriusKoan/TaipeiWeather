from flask import Flask, Blueprint
from flask_cors import CORS
import config
from app import main


def create_app(config_name):
    app = Flask("app")
    app.config.from_object(config.config_list[config_name])
    CORS(app)
    app.register_blueprint(main)
    return app