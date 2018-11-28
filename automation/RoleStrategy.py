# Library imports
import requests

# Internal imports
from automation.JenkinsCore import JenkinsCore

# =============================================================================================== #
#                                           Classe
# =============================================================================================== #


class RoleStrategy:
    """
        Classe de mapeamento da API do plugin role-strategy
    """
    def __init__(self, jenkins: JenkinsCore, debug=False):
        """
            Metodo construtor
            :param debug:
            :param jenkins:     Recebe uma instancia da classe JenkinsCore
        """
        self.debug = debug
        self.jenkins = jenkins
        self.environments = self.jenkins.getEnvironments()
        self.bUrl = 'http://{0}@{1}/role-strategy/strategy'.format(self.jenkins.get_bAuth(), self.jenkins.get_url())

    def get_role(self, type: str = None, name: str = None) -> requests:
        """
            Funcao para retornar uma role especifica de um tipo especifico
            :param type:        Recebe o tipo de role
            :param name:        Recebe o nome da role
            :return:            Retorna objeto response
        """
        data = dict(type=type, roleName=name)
        response = requests.post(url='{0}/getRole'.format(self.bUrl), params=data)
        if self.debug:
            self.analise_content(data=data, response=response)
        return response

    def get_all_roles(self, type: str = None) -> requests:
        """
            Funcao para buscar todas as roles de um tipo especifico
            :param type:        Recebe o tipo da role
            :return:            Retorna objeto response
        """
        data = dict(type=type)
        response = requests.post(url='{0}/getAllRoles'.format(self.bUrl), params=data)
        if self.debug:
            self.analise_content(data=data, response=response)
        return response

    def create_role(self, type: str = None, name: str = None, pattern: str = None, perm: str = None,
                    overwrite: bool = False) -> requests:
        """
            Funcao para criacao das roles
            :param type:        Recebe o tipo da role
            :param name:        Recebe o nome da role
            :param pattern:     Recebe o padrao da role
            :param perm:        Recebe as permissoes da role
            :param overwrite:   Opcao para sobrescrever role caso ja exista
            :return:            Retorna objeto response
        """
        data = dict(type=type, roleName=name, pattern=pattern, permissionIds=perm, overwrite=overwrite)
        response = requests.post(url='{0}/addRole'.format(self.bUrl), params=data)
        if self.debug:
            self.analise_content(data=data, response=response)
        return response

    def delete_role(self, type: str = None, name_list: str = None) -> requests:
        """
            Funcao para remocao da(s) role(s)
            :param type:        Recebe o tipo da(s) role(s)
            :param name_list:   Recebe uma lista de role(s) (convertido para string - Compatibilidade)
            :return:            Retorna objeto response
        """
        data = dict(type=type, roleNames=name_list)
        response = requests.post(url='{0}/removeRoles'.format(self.bUrl), params=data)
        if self.debug:
            self.analise_content(data=data, response=response)
        return response

    def assing_role(self):
        pass

    def unassing_role(self):
        pass

    def analise_content(self, data: dict = None, response: requests = None) -> None:
        """
            Funcao para debug das funcoes
            :param data:        Recebe o conteudo/payload/parameters da chamada
            :param response:    Recebe o response
            :return:            Nada
        """
        print("Data gathered:")
        print("- Data: {0}".format(str(data)))
        print("- Request URL: {0}".format(response.url))
        print("- Response:")
        print("\t- Code: {0}".format(response.status_code))
        print("\t- Content: {0}".format(str(response.content)))

# =============================================================================================== #
