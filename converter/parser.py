from typing import Generator
from github import Github
from urllib.parse import urlparse, urlsplit


def get_file_name(url: str) -> str:
    url_schem = urlsplit(url)
    delimetr = 'master'
    if '.' in url_schem.path.split('/')[-1]:
        if 'main' in url_schem.path:
            delimetr = 'main'
        path_to_file = urlsplit(url).path.split(delimetr)[-1]
        return path_to_file.replace('/', '', 1)
    else:
        return ''


def parse(url: str) -> Generator:
    g = Github()
    user_repo = urlparse(url).path.split('/')
    repo = g.get_repo(f'{user_repo[1]}/{user_repo[2]}')
    filename = get_file_name(url)
    content = repo.get_contents(filename)
    if filename:
        yield content.download_url
    while content and isinstance(content, list):
        file_content = content.pop(0)
        if file_content.type == 'dir':
            content.extend(repo.get_contents(file_content.path))
        elif file_content.path.endswith('.md') or \
                file_content.path.endswith('.rtf'):
            yield file_content.download_url
