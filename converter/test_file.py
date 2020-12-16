import os
import urllib
import tempfile

import pypandoc

from converter.app import flask_app

# url_path = r'https://raw.githubusercontent.com/awsdocs/amazon-api-gateway-developer-guide/main/doc_source/amazon-api-gateway-using-stage-variables.md'
#
# a, b = os.path.split(url_path)
#
#
# # tmp = tempfile.NamedTemporaryFile(dir=flask_app.config['UPLOAD_FOLDER'], suffix='.md')
#
# with tempfile.NamedTemporaryFile(dir=flask_app.config['UPLOAD_FOLDER'], suffix='.md') as tmp:
#     with urllib.request.urlopen(url_path) as file:
#         tmp.write(file.read())
#         tmp.seek(0)
#         pypandoc.convert_file(tmp.name, 'epub', outputfile=r'C:\Users\Anton_Tsyhankou\PycharmProjects\epubconverter\instance\CONTRIBUTING.epub')
