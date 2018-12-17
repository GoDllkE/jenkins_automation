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
        """
            Funcao GET da url padrao do jenkins
            :return:    retorna URL
        """
        return self.url

    def get_user(self) -> str:
        """
            Funcao GET do usuario BOT do jenkins
            :return:    retorna nome do usuario
        """
        return self.username

    def get_passwd(self) -> str:
        """
            funcao GET da senha do usuario BOT
            :return:    retorna senha do usuario
        """
        return self.password

    def get_bauth(self) -> str:
        """
            funcao GET da formatacao HTTP_BASIC_AUTH com usuario BOT
            :return:    retorna HTTP_BASIC_AUTH do usuario
        """
        return self.b_auth

    def get_environments(self) -> list:
        """
            funcao GET da lista de ambientes disponiveis no jenkins
            :return:    retorna lista de ambientes
        """
        return self.environment

    def get_burl(self) -> list:
        """
            funcao GET da url do jenkins contendo uma HTTP_BASIC_AUTH
            :return:    retorna url formatada para requisicoes http via biblioteca requests
        """
        return "http://{0}@{1}".format(self.get_bauth(), self.get_url())

    # =============================================================================================== #
