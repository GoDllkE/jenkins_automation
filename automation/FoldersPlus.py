# Library imports
import sys
import requests

# Internal imports
from automation import JenkinsCore


class FoldersPlus:

    def __init__(self, jenkins: JenkinsCore, debug=False):
        """
        Metodo construtor
        :param debug:           Parametro de definição de debug
        :param jenkins:         Recebe uma instancia da classe JenkinsCore
        """
        self.debug = debug
        self.jenkins = jenkins
        self.bUrl = 'http://{0}@{1}/job/projects'.format(self.jenkins.get_bauth(), self.jenkins.get_url())

    # ================================================================================================================ #
    #                                                   Core                                                           #
    # ================================================================================================================ #

    def create_structure(self, path: str = None, name: str = None) -> requests:
        # Controle interno
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"name": "{0}".format(name), "mode": "com.cloudbees.hudson.plugins.folder.Folder", "Submit": "OK"}
        response = requests.post(url="{0}{1}".format(self.bUrl, path), headers=header, params=data)
        if self.debug:
            self.analise_content(data=data, response=response)
        return response

    def delete_structure(self, name: str = None) -> requests:
        response = requests.post(url="{0}/job/{1}/doDelete".format(self.bUrl, name))
        if self.debug:
            self.analise_content(data={}, response=response)
        return response
        pass

    # ================================================================================================================ #
    #                                                 Miscellaneous                                                    #
    # ================================================================================================================ #

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

    def validate(self, status_code: int = None, folder: str = None, env: str = None) -> None:
        """
            Funcao que valida o status_code das requisicoes
            :param status_code:     Recebe o status code de um objeto request
            :param folder:          Recebe o path do objeto que foi requisitado a ser criado
            :param env:             (Opcional) Recebe nome do ambiente
            :return:                Retorna Nada.
        """
        if status_code == 200:
            print('concluido com sucesso!')
        elif status_code == 400:
            if env:
                print('erro de operação. Pasta "{0}" ja existe'.format(folder.replace('<env>', env)))
            else:
                print('erro de operação. Pasta "{0}" ja existe'.format(folder))
        else:
            if env:
                print('erro. Nao foi possivel localizar pasta "{0}" (codigo: {1})'.format(folder.replace('<env>', env), status_code))
            else:
                print('erro. Nao foi possivel localizar pasta "{0}" (codigo: {1})'.format(folder, status_code))
            sys.exit(1)
        pass

    # ================================================================================================================ #
