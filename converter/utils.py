import io
import os
import urllib.parse
from werkzeug.utils import secure_filename
from converter.converter_2_pdf import generate_new_name, process_content,\
     convert_to_user_format


def allowed_file(some_obj) -> bool:
    """Return True if extension is allowed or if link on repo"""
    allowed_extens = ['md', 'rtf']
    if some_obj.startswith('http://') or some_obj.startswith('https://'):
        url_schema = urllib.parse.urlparse(some_obj)
        if '.' in url_schema.path.split('/')[-1]:
            return url_schema.path.split('.')[-1] in allowed_extens
        else:
            return True
    else:
        return '.' in some_obj and some_obj.split('.')[-1] in allowed_extens


def get_content(flask_request):
    file = flask_request.files.get('file')
    url = flask_request.form.get('url')
    file_name = url or secure_filename(file.filename)
    output_format = flask_request.form.get('formatList')
    if allowed_file(file_name):
        new_filename = generate_new_name(file_name, output_format)
        convert_to_user_format(process_content(file, url), new_filename)
        return new_filename


def copy_file_and_remove(filename: str):
    file_like_object = io.BytesIO()
    with open(filename, 'rb') as f:
        file_like_object.write(f.read())
        file_like_object.seek(0)
    os.remove(filename)
    return file_like_object
