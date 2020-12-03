from github import Github

g = Github()
requested_list = None
repo = g.get_repo('Barmatux/cosmoport')
content = repo.get_contents('')
while content:
    file_content = content.pop(0)
    if file_content.type == 'dir':
        content.extend(repo.get_contents(file_content.path))
    elif file_content.path.split('.')[1] == 'md':
        if not requested_list:
            requested_list = [file_content]
        else:
            requested_list.append(file_content)
