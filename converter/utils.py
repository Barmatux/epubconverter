import io
import os
import urllib.parse
from werkzeug.utils import secure_filename
from converter.parser import prepare_book_chp, join_files
from converter.converter_to_pdf import generate_new_name, process_content, \
    convert_to_user_format


def allowed_file(some_obj) -> bool:
    allowed_extens = ['md', 'rtf']
    if some_obj.startswith('http://') or some_obj.startswith('https://'):
        url_schema = urllib.parse.urlparse(some_obj)
        return url_schema.path.split('.')[-1] in allowed_extens
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


def copy_in_memory(filename: str) -> io.BytesIO:
    file_like_object = io.BytesIO()
    with open(filename, 'rb') as f:
        file_like_object.write(f.read())
        file_like_object.seek(0)
    os.remove(filename)
    return file_like_object


def process_repo_url(flask_request):
    url = flask_request.form.get('url')
    output_format = flask_request.form.get('formatList')
    new_name = generate_new_name(url, output_format)
    chap_lst, tmpdir = prepare_book_chp(url)
    join_files(chap_lst, tmpdir, new_name)
    return new_name
