from converter.app import flask_app
from flask import render_template, request, redirect, url_for
from flask import send_from_directory
from converter.converter_2_pdf import create_epub
from converter.utils import allowed_file


@flask_app.route('/', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        file = request.files.get('file')
        url = request.form.get('url')
        if file and allowed_file(file.filename):
            file_name = create_epub(file)
        elif url and allowed_file():
            file_name = create_epub(url)
        else:
            return redirect('/exception')
        return redirect(url_for('uploaded_file', filename=file_name))
    return render_template('index.html')


@flask_app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(flask_app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


@flask_app.route('/exception')
def exception_page():
    return "Something goes wrong"
