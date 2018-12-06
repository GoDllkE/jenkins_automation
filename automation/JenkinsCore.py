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
        self.bAuth = '{0}:{1}'.format(self.username, self.password)

    # =============================================================================================== #
    #                                           Metodos
    # =============================================================================================== #

    def get_url(self) -> str:
        return self.url

    def get_user(self) -> str:
        return self.username

    def get_passwd(self) -> str:
        return self.password

    def get_bAuth(self) -> str:
        return self.bAuth

    def getEnvironments(self) -> list:
        return self.environment

    def get_bUrl(self) -> list:
        return "{0}@{1}".format(self.get_bAuth(), self.get_url())