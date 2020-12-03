import os
import tempfile
import urllib
import urllib.parse
import pypandoc
from converter.app import flask_app


def read_stream(path):
    """Return stream for writing"""
    if isinstance(path, str):
        with urllib.request.urlopen(path) as file:
            return file.read()
    else:
        return path.stream.read()


def create_epub(path_to_file: str) -> str:
    """Creating epub file"""
    with tempfile.NamedTemporaryFile(dir=flask_app.config['UPLOAD_FOLDER'], suffix='.md') as tmp:
        tmp.write(read_stream(path_to_file))
        tmp.seek(0)
        file_name = convert(tmp.name, path_to_file)
    return file_name


def change_name(path_to_file):
    """Return original name of the file"""
    if isinstance(path_to_file, str):
        split_url = urllib.parse.urlsplit(path_to_file)
        origin_file_name = split_url.path.split('/')[-1]
        return origin_file_name.replace(origin_file_name.split('.')[-1], 'epub')
    else:
        or_file_name = os.path.split(path_to_file.filename)[-1]
        return or_file_name.replace(or_file_name.split('.')[-1], 'epub')


def convert(url_path: str, original_path: str) -> str:
    """ Return new file name"""
    new_name = change_name(original_path)
    converted_path = url_path.replace(os.path.split(url_path)[-1], new_name)
    pypandoc.convert_file(url_path, 'epub', outputfile=converted_path)
    return new_name
