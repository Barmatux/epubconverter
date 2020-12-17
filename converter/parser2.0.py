import os
import tempfile

import pypandoc
from github import Github
from pprint import pprint
import urllib.request
import urllib.parse
import tempfile

TOKEN = '670c1c294a1889431e53ad37ea6d5814b7ecc972'
RAW_ADRESS = r'raw.githubusercontent.com'

g = Github(TOKEN)
requested_list = None
repo = g.get_repo('awsdocs/amazon-api-gateway-developer-guide')
content = repo.get_contents('')
# while content:
#     file_content = content.pop(0)
#     if file_content.type == 'dir':
#         content.extend(repo.get_contents(file_content.path))
#     elif file_content.path[-2:] == 'md':
#         print(content[0].name)
#         print(content[0].html_url)
#         break

with tempfile.NamedTemporaryFile(suffix='.md') as tmp:
    while content:
        file_content = content.pop(0)
        if file_content.type == 'dir':
            content.extend(repo.get_contents(file_content.path))
        elif file_content.path.endswith('md'):
            schema = urllib.parse.urlsplit(file_content.html_url)
            new_schema = schema._replace(netloc=RAW_ADRESS)
            new_str = new_schema.path
            new_str = new_str.replace('/blob', '')
            new_schema = new_schema._replace(path=new_str)
            result = urllib.parse.urlunsplit(new_schema)
            with urllib.request.urlopen(result) as f:
                tmp.write(f.read())

pypandoc.convert_file(tmp.name, 'epub', outputfile=r'D:\test.epub')



# for url_address in requested_list:
#     url_components = urllib.parse.urlparse(url_address)
#     pprint(url_components.path)
#     file_path = os.path.join('D:\\test', url_address.rsplit('/')[-1])
#     with open (r'D:\test2.md', 'ab') as file:
#         tmp = tempfile.NamedTemporaryFile()
#         print(tmp.name)
#         with urllib.request.urlopen(url_address) as f:
#             file.write(f.read())


#
# def many_to_one(path: str) -> str:
#     directory = os.fsencode(path)
#     filename = r'D:\\test.md'
#     with open(filename, 'a') as f:
#         for i in os.listdir(directory):
#             path_to_file = os.path.join(directory, i)
#             print(path_to_file)
#             with open(path_to_file, 'r') as file:
#                 print('you are here')
#                 f.write(file.read())
#                 f.write('-' * 30)
#     return filename


# a = r'https://github.com/awsdocs/aws-doc-sdk-examples/blob/master/cpp/README.rst'
# b = r'raw.githubusercontent.com'
# schema = urllib.parse.urlsplit(a)
# new_schema = schema._replace(netloc=b)
# result = urllib.parse.urlunsplit(new_schema)
# print(result)