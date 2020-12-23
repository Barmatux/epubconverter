import urllib.parse
from flask import request, redirect
import io
import os
from werkzeug.utils import secure_filename
from converter.converter_2_pdf import process_file, process_url, generate_new_name


def allowed_file(some_obj) -> bool:
    allowed_extensions = ['md', 'rtf']
    if isinstance(some_obj, str):
        url_schema = urllib.parse.urlparse(some_obj)
        return url_schema.path.split('.')[-1] in allowed_extensions
    else:
        return '.' in some_obj.filename and some_obj.filename.split('.')[-1] in allowed_extensions


def get_content(flask_request: request) -> tuple[bytes, str]:
    file = flask_request.files.get('file')
    url = flask_request.form.get('url')
    output_format = flask_request.form.get('formatList')
    if file and allowed_file(file):
        file_name = secure_filename(file.filename)
        return process_file(file), generate_new_name(file_name, output_format)
    elif url and allowed_file(url):
        return process_url(url), generate_new_name(url, output_format)
    else:
        return redirect('/exception')


def copy_file_and_remove(filename: str):
    file_like_object = io.BytesIO()
    with open(filename, 'rb') as f:
        file_like_object.write(f.read())
        file_like_object.seek(0)
    os.remove(filename)
    return file_like_object
