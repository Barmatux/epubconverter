from github import Github
from pprint import pprint

TOKEN = '670c1c294a1889431e53ad37ea6d5814b7ecc972'


g = Github(TOKEN)
requested_list = None
repo = g.get_repo('Barmatux/cosmoport')
content = repo.get_contents('')
while content:
    file_content = content.pop(0)
    # print(type(file_content.path))
    # print('-'* 50)
    if file_content.type == 'dir':
        content.extend(repo.get_contents(file_content.path))
    elif file_content.path.split('.')[1] == 'md':
        if not requested_list:
            requested_list = [file_content]
        else:
            requested_list.append(file_content)

print(requested_list[0].html_url)

# with open ('test27.txt', 'wb') as file:
#     for i in requested_list:
#         file.write(i)
#         pprint(i)
