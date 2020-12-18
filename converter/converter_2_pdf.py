import os
import tempfile
import urllib
import urllib.parse
from pypandoc import convert_file


def process_file(file) -> bytes:
    return file.stream.read()


def process_url(url: str) -> bytes:
    with urllib.request.urlopen(url) as file:
        return file.read()


def convert_to_user_format(bytes_stream: bytes, new_file_name: str) -> str:
    """Creating epub file"""
    with tempfile.NamedTemporaryFile(dir=os.getcwd(), suffix='.md') as tmp:
        tmp.write(bytes_stream)
        tmp.seek(0)
        convert(tmp.name, new_file_name)
    return new_file_name


def change_name(filename: str, output_format: str):
    """Return original name of the file"""
    if r'https:\\' or r'http:\\' in filename:
        split_url = urllib.parse.urlsplit(filename)
        origin_file_name = split_url.path.split('/')[-1]
    else:
        origin_file_name = os.path.split(filename)[-1]
    return origin_file_name.replace(origin_file_name.split('.')[-1], output_format)


def convert(path_to_file: str, new_file_name: str):
    """ Return new file name"""
    converted_path = path_to_file.replace(os.path.split(path_to_file)[-1], new_file_name)
    convert_file(path_to_file, new_file_name.split('.')[-1], outputfile=converted_path)
