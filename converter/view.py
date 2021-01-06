from converter.app import flask_app
import mimetypes
from flask import render_template, request, redirect, url_for, send_file
from converter.utils import get_content, copy_file_and_remove


@flask_app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        try:
            new_file_name = get_content(request)
            if not new_file_name:
                raise AttributeError
        except AttributeError:
            return redirect(url_for('exception_page'))
        return redirect(url_for('uploaded_file', filename=new_file_name))
    return render_template('index.html')


@flask_app.route('/uploads/<filename>')
def uploaded_file(filename):
    mimetype, encoding = mimetypes.guess_type(filename)
    return_data = copy_file_and_remove(filename)
    return send_file(return_data, mimetype=mimetype)


@flask_app.route('/convert-repo', methods=['GET', 'POST'])
def converted_page():
    if request.method == 'POST':
        filename = get_content(request)
        return redirect(url_for('uploaded_file', filename=filename))
    return render_template('convert_repo.html')


@flask_app.route('/exception')
def exception_page():
    return "Something goes wrong"
