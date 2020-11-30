from converter.app import flask_app
from flask import render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory
import os
from converter.converter_2_pdf import Converter


ALLOWED_EXTENSIONS = ['md', 'rtf', 'pdf']


def allowed_file(filename: str) -> bool:
    return '.' in filename and filename.split('.')[1] in ALLOWED_EXTENSIONS


def convert_to_pdf(address: str) -> None:
    converter = Converter()
    converter.convert(address)


def get_new_filename(name: str) -> str:
    if '/' in name:
        return name.split('/')[-1].replace(name[-2:], 'epub')
    return name.replace(name[-2:], 'epub')


@flask_app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        file = request.files.get('file')
        url = request.form.get('url')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(flask_app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            convert_to_pdf(file_path)
            return redirect(url_for('uploaded_file', filename=get_new_filename(filename)))
        elif url:
            convert_to_pdf(url)
            return redirect(url_for('uploaded_file', filename=get_new_filename(url)))
    return render_template('index.html')


@flask_app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(flask_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@flask_app.route('/oops')
def url_rend():
    return "Oops i haven't done yet"
