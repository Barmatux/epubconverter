import requests
import urllib.parse
import re
from typing import List, Dict, Union
from converter.github_client.content_file import Content
from converter.github_client.repository import Repository

BASE_URL = 'https://api.github.com'


class ConvGitHub:
    def __init__(self,
                 token=None,
                 base_url=BASE_URL):
        self.headers = self._get_headers(token)
        self.base_url = base_url

    def _get_headers(self, token: str) -> Union[Dict, str]:
        if token:
            return {'Authorization': f'token {token}'}
        return ''

    def _get_user(self, url: str) -> str:
        """Return user name"""
        sch = urllib.parse.urlsplit(url)
        pattern = r'[^/]+'
        user = re.search(pattern, sch.path)
        return user.group(0)

    def _get_user_and_repo(self, url: str) -> str:
        """return user/repo string"""
        sch = urllib.parse.urlsplit(url)
        pattern = r'[^/]([^/]*/[^/]*)'
        user_repo = re.search(pattern, sch.path)
        return user_repo.group(0)

    def get_repo(self, url: str) -> Repository:
        """Return repository"""
        user_repo = self._get_user_and_repo(url)
        url = f'/repos/{user_repo}'
        res_url = urllib.parse.urljoin(self.base_url, url)
        resp = self._send_get_request(res_url)
        return Repository(resp)

    def _send_get_request(self, url: str) -> List[Dict]:
        resp = requests.get(url, self.headers)
        return resp.json()

    def get_lst_users_repo(self, user_url: str) -> List[Repository]:
        """Return all repositories of a user"""
        user = self._get_user(user_url)
        url = f'/users/{user}/repos'
        res_url = urllib.parse.urljoin(self.base_url, url)
        res = requests.get(res_url, headers=self.headers)
        repos = res.json()
        while 'next' in res.links.keys():
            res = requests.get(res.links['next']['url'])
            repos.extend(res.json())
        return [Repository(repo) for repo in repos]

    def get_repo_content(self, url: str, path: str = None) -> List[Content]:
        """Recursively find all files in a repository"""
        if not path:
            path = ''
        user_and_repo = self._get_user_and_repo(url)
        url_query = f'/repos/{user_and_repo}/contents/{path}'
        res_url = urllib.parse.urljoin(self.base_url, url_query)
        content_lst = None
        resp = self._send_get_request(res_url)
        res_lst = [Content(cont) for cont in resp]
        # todo: spit function, make it more readable
        while res_lst:
            cont = res_lst.pop(0)
            if cont.type == 'dir':
                path = cont.name
                res_lst.extend(self.get_repo_content(url, path))
            else:
                if content_lst:
                    content_lst.append(cont)
                else:
                    content_lst = [cont]
        return content_lst
