#


class JenkinsCore:
    """
        Classe de definicao do Jenkins
    """
    def __init__(self, url: str = 'jenkins-central.pontoslivelo.com.br',
                 username: str = 'S00000001', password: str = 'R0xbV0p7UIjNTFte'):
        #
        self.url = url

        # Define o usuario da instancia (padrão usuario: BOT)
        self.username = username
        self.password = password

        # Define ambientes
        self.environment = ['dev', 'sit', 'uat', 'prd']

        # Generate basic-auth
        self.b_auth = '{0}:{1}'.format(self.username, self.password)

    # =============================================================================================== #
    #                                           Métodos
    # =============================================================================================== #

    def get_url(self) -> str:
        return self.url

    def get_user(self) -> str:
        return self.username

    def get_passwd(self) -> str:
        return self.password

    def get_bauth(self) -> str:
        return self.b_auth

    def get_environments(self) -> list:
        return self.environment

    def get_burl(self) -> list:
        return "http://{0}@{1}".format(self.get_bauth(), self.get_url())

    # =============================================================================================== #
