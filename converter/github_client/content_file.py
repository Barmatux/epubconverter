class Content:
    def __init__(self, cont):
        self.cont = cont

    def __repr__(self):
        return self.cont['path']

    @property
    def content(self):
        return self.cont['content']

    @property
    def html_url(self):
        return self.cont['html_url']

    @property
    def download_url(self):
        return self.cont['download_url']

    @property
    def name(self):
        return self.cont['name']

    @property
    def type(self):
        return self.cont['type']

    @property
    def sha(self):
        return self.cont['sha']
