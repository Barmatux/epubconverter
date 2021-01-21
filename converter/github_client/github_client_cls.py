import requests
import urllib.parse
import re
from typing import List, Dict, Union
from converter.github_client.content_file import Content
from converter.github_client.repository import Repository


class ConvGitHub:
    def __init__(self,
                 token=None,
                 base_url='https://api.github.com'):
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

    def get_content(self, url: str, path: str = '') \
            -> Union[Content, List[Content]]:
        """Recursively find all files in a repository"""
        user_and_repo = self._get_user_and_repo(url)
        url_query = f'/repos/{user_and_repo}/contents/{path}'
        res_url = urllib.parse.urljoin(self.base_url, url_query)
        resp = self._send_get_request(res_url)
        if isinstance(resp, list):
            return self._get_all_repo_cont(url, resp)
        return Content(resp)

    def _get_all_repo_cont(self, url, resp):
        cont_lst = [Content(file) for file in resp]
        res_cont_lst = None
        while cont_lst:
            cont = cont_lst.pop(0)
            if cont.type == 'dir':
                path = cont.name
                cont_lst.extend(self.get_content(url, path))
            else:
                if res_cont_lst:
                    res_cont_lst.append(cont)
                else:
                    res_cont_lst = [cont]
        return res_cont_lst
