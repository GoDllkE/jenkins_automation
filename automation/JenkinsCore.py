#


class JenkinsCore:

    def __init__(self, url: str = None, username: str = None, password: str = None):
        self.url = url
        self.username = username
        self.password = password
        self.bAuth = '{0}:{1}'.format(username, password)
        pass

    def get_url(self):
        return self.url

    def get_uer(self):
        return self.username

    def get_passwd(self):
        return self.password

    def get_bAuth(self):
        return self.bAuth