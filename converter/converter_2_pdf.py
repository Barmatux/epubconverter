import os
import tempfile
import urllib
import urllib.parse
from pypandoc import convert_file
from typing import Optional


def _read_stream(path):
    """Return stream for writing"""
    if isinstance(path, str):
        with urllib.request.urlopen(path) as file:
            return file.read()
    else:
        return path.stream.read()


def convert_to_user_format(path_to_file, output_format: str) -> str:
    """Creating epub file"""
    with tempfile.NamedTemporaryFile(dir=os.getcwd(), suffix='.md') as tmp:
        tmp.write(_read_stream(path_to_file))
        tmp.seek(0)
        file_name = convert(tmp.name, path_to_file, output_format)
    return file_name


def _change_name(path_to_file: Optional, output_format: str):
    """Return original name of the file"""
    if isinstance(path_to_file, str):
        split_url = urllib.parse.urlsplit(path_to_file)
        origin_file_name = split_url.path.split('/')[-1]
    else:
        origin_file_name = os.path.split(path_to_file.filename)[-1]
    return origin_file_name.replace(origin_file_name.split('.')[-1], output_format)


def convert(url_path: str, original_path: str, output_format: str) -> str:
    """ Return new file name"""
    new_name = _change_name(original_path, output_format)
    converted_path = url_path.replace(os.path.split(url_path)[-1], new_name)
    convert_file(url_path, output_format, outputfile=converted_path)
    return new_name
