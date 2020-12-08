import urllib.parse


def allowed_file(some_obj) -> bool:
    allowed_extensions = ['md', 'rtf']
    if isinstance(some_obj, str):
        url_schema = urllib.parse.urlparse(some_obj)
        return url_schema.path.split('.')[-1] in allowed_extensions
    else:
        return '.' in some_obj.filename and some_obj.filename.split('.')[-1] in allowed_extensions


def get_mimetype(filename):
    return filename.split('.')[-1]
