class Repository:
    def __init__(self, repo_content):
        self.repo_content = repo_content

    def __repr__(self):
        return self.repo_content['name']

    @property
    def name(self):
        return self.repo_content['name']

    @property
    def full_name(self):
        return self.repo_content['full_name']

    @property
    def download_url(self):
        return self.repo_content['download_url']

    @property
    def url(self):
        return self.repo_content['url']

    @property
    def clone_url(self):
        return self.repo_content['clone_url']
