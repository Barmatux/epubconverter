from converter.app import flask_app
import mimetypes
from flask import render_template, request, redirect, url_for, send_file
from converter.converter_2_pdf import convert_to_user_format
from converter.utils import get_content, copy_file_and_remove


@flask_app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        some_obj, new_file_name = get_content(request)
        convert_to_user_format(some_obj, new_file_name)
        return redirect(url_for('uploaded_file', filename=new_file_name))
    return render_template('index.html')


@flask_app.route('/uploads/<filename>')
def uploaded_file(filename):
    mimetype, encoding = mimetypes.guess_type(filename)
    return_data = copy_file_and_remove(filename)
    return send_file(return_data, mimetype=mimetype)


@flask_app.route('/exception')
def exception_page():
    return "Something goes wrong"
