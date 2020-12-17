import io
from converter.app import flask_app
from flask import render_template, request, redirect, url_for, send_file
from converter.converter_2_pdf import convert_to_user_format
from converter.utils import allowed_file, get_mimetype
import os


@flask_app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        file = request.files.get('file')
        url = request.form.get('url')
        output_format = request.form.get('formatList')
        some_obj = file if file else url
        if allowed_file(some_obj) and some_obj:
            file_name = convert_to_user_format(some_obj, output_format)
        else:
            return redirect('/exception')
        return redirect(url_for('uploaded_file', filename=file_name))
    return render_template('index.html')


@flask_app.route('/uploads/<filename>')
def uploaded_file(filename):
    mime_type = get_mimetype(filename)
    ret_data = io.BytesIO()
    with open(filename, 'rb') as f:
        ret_data.write(f.read())
        ret_data.seek(0)
    os.remove(filename)
    return send_file(ret_data, mimetype=mime_type)


@flask_app.route('/exception')
def exception_page():
    return "Something goes wrong"
