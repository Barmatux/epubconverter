def allowed_file(filename: str) -> bool:
    allowed_extensions = ['md', 'rtf']
    return '.' in filename and filename.split('.')[1] in allowed_extensions
