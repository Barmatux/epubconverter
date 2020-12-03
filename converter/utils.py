import urllib.parse


def allowed_file(filename: str) -> bool:
    allowed_extensions = ['md', 'rtf']
    if filename.startswith(r'https:\\') or filename.startswith(r'http:\\'):
        url_schema = urllib.parse.urlparse(filename)
        return url_schema.path.split('.')[-1] in allowed_extensions
    else:
        return '.' in filename and filename.split('.')[-1] in allowed_extensions
