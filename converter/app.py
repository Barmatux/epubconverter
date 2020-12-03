from flask import Flask


flask_app = Flask(__name__)
flask_app.config['DEBUG'] = True
flask_app.config['UPLOAD_FOLDER'] = flask_app.instance_path
