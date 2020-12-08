from flask import Flask
from config import Configuration

flask_app = Flask(__name__)
flask_app.config.from_object(Configuration)
