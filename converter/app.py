from flask import Flask
from converter import  converter_2_pdf
from converter.config import Configuration


flask_app = Flask(__name__)
# flask_app.config.from_object(Configuration)
flask_app.config['DEBUG'] = True
flask_app.config['UPLOAD_FOLDER'] = flask_app.instance_path

