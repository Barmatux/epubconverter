import urllib.parse
from werkzeug.utils import secure_filename


def allowed_file(some_obj) -> bool:
    allowed_extensions = ['md', 'rtf']
    if isinstance(some_obj, str):
        url_schema = urllib.parse.urlparse(some_obj)
        return url_schema.path.split('.')[-1] in allowed_extensions
    filename = secure_filename(some_obj.filename)
    return '.' in filename and filename.split('.')[-1] in allowed_extensions


def get_mimetype(filename):
    return filename.split('.')[-1]
