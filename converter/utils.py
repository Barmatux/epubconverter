import urllib.parse
from flask import request, redirect
import io
import os
from converter.converter_2_pdf import process_file, process_url, change_name
from werkzeug.utils import secure_filename


def allowed_file(some_obj) -> bool:
    allowed_extensions = ['md', 'rtf']
    if isinstance(some_obj, str):
        url_schema = urllib.parse.urlparse(some_obj)
        return url_schema.path.split('.')[-1] in allowed_extensions
    else:
        return '.' in some_obj.filename and some_obj.filename.split('.')[-1] in allowed_extensions


def get_mimetype(filename: str) -> str:
    return filename.split('.')[-1]


def get_content(flask_request: request) -> tuple[bytes, str]:
    file = flask_request.files.get('file')
    url = flask_request.form.get('url')
    output_format = flask_request.form.get('formatList')
    if file and allowed_file(file):
        file_name = secure_filename(file.filename)
        return process_file(file), change_name(file_name, output_format)
    elif url and allowed_file(url):
        return process_url(url), change_name(url, output_format)
    else:
        return redirect('/exception')


def copy_file_and_remove(filename: str) -> tuple:
    mime_type = get_mimetype(filename)
    ret_data = io.BytesIO()
    with open(filename, 'rb') as f:
        ret_data.write(f.read())
        ret_data.seek(0)
    os.remove(filename)
    return mime_type, ret_data
