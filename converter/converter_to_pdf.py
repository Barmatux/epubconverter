import os
import tempfile
import urllib
import urllib.parse
from pypandoc import convert_file
import re


def process_content(file=None, url: str = None) -> bytes:
    """read file"""
    if file:
        return file.stream.read()
    with urllib.request.urlopen(url) as conn:
        return conn.read()


def convert_to_user_format(bytes_stream: bytes, new_file_name: str) -> None:
    """Creating epub file"""
    with tempfile.NamedTemporaryFile(dir=os.getcwd(), suffix='.md') as tmp:
        tmp.write(bytes_stream)
        convert(tmp.name, new_file_name)


def generate_new_name(filename: str, output_format: str) -> str:
    """Return new name of the file"""
    if re.match(r'(https*://)', filename):
        split_url = urllib.parse.urlsplit(filename)
        origin_file_name = split_url.path.split('/')[-1]
    else:
        origin_file_name = os.path.split(filename)[-1]
    if '.' in origin_file_name:
        return origin_file_name.replace(
            origin_file_name.split('.')[-1], output_format)
    else:
        return '.'.join((origin_file_name, output_format))


def convert(path_to_file: str, new_file_name: str) -> None:
    """ Convert file into epub format"""
    extension = new_file_name.split('.')[-1]
    convert_file(path_to_file, extension, outputfile=new_file_name)
