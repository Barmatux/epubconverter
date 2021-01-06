import os
import tempfile
import urllib
import urllib.parse
from pypandoc import convert_file
from converter.parser import parse


def process_content(file=None, url: str = None):
    """read file"""
    if file:
        yield file.stream.read()
    else:
        for doc in parse(url):
            with urllib.request.urlopen(doc) as file:
                yield file.read()


def convert_to_user_format(gen_bytes_stream, new_file_name: str):
    """Creating epub file"""
    with tempfile.NamedTemporaryFile(
             mode='a+b', dir=os.getcwd(), suffix='.md') as tmp:
        for i in gen_bytes_stream:
            tmp.write(i)
        convert(tmp.name, new_file_name)


def generate_new_name(filename: str, output_format: str):
    """Return new name of the file"""
    if filename.startswith(r'https://') or filename.startswith(r'http://'):
        split_url = urllib.parse.urlsplit(filename)
        origin_file_name = split_url.path.split('/')[-1]
    else:
        origin_file_name = os.path.split(filename)[-1]
    if '.' in origin_file_name:
        return origin_file_name.replace(
            origin_file_name.split('.')[-1], output_format)
    else:
        return '.'.join((origin_file_name, output_format))


def convert(path_to_file: str, new_file_name: str):
    """ Convert file into epub format"""
    extension = new_file_name.split('.')[-1]
    convert_file(path_to_file, extension, outputfile=new_file_name)
