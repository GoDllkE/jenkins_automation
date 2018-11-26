#


class JenkinsCore:

    def __init__(self, url: str = None, username: str = None, password: str = None):
        #
        self.url = url

        if username is None:
            self.username = 'S00000001'
        else:
            self.username = username

        if password is None:
            self.password = 'R0xbV0p7UIjNTFte'
        else:
            self.password = password

        # Generate basic-auth
        self.bAuth = '{0}:{1}'.format(self.username, self.password)
        pass

    def get_url(self):
        return self.url

    def get_user(self):
        return self.username

    def get_passwd(self):
        return self.password

    def get_bAuth(self):
        return self.bAuth
