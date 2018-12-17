#
import sys
import requests

from automation import JenkinsCore

# Variavel de controle de desenvolvimento e depuração
development_control = False


class StashCore:

    def __init__(self, jenkins: JenkinsCore = None, debug: bool = None):
        self.debug = debug
        self.jenkins = jenkins
        self.b_url = 'https://{0}:{1}@stash.pontoslivelo.com.br/rest/api/1.0' \
            .format(self.jenkins.get_user(), self.jenkins.get_passwd())
        pass

    def __get_all_projects__(self) -> dict:
        """
            Funcao de requisição para API do bitbucket
            Referencia: https://stash.pontoslivelo.com.br/plugins/servlet/restbrowser#/resource/api-1-0-projects/GET
            :return:            Retorna dicionario com a lista de projetos
        """
        data = dict(limit=1000, size=1000)
        response = requests.get(url='{0}/projects'.format(self.b_url), params=data)
        if self.validate(status_code=response.status_code):
            if self.debug:
                self.analise_content(response=response, data=data)
            return response.json()
        else:
            sys.exit(1)

    def get_project_name(self, project_id: str = None) -> str:
        """
            Funcao de parseamento do resultado da lista de projetos
            :param project_id:          ID do projeto no stash da qual deseja encontrar o displayName
            :return:                    Retorna uma STR com o nome do projeto referente a ID passada.
        """
        data = self.__get_all_projects__()
        project_id = project_id.upper()

        # Parse results
        for project in data['values']:
            if project['key'] == project_id:
                return project['name']
        return None

    def get_project_id(self, project_name: str = None) -> str:
        """
            Funcao de parseamento do resultado da lista de projetos
            :param project_name:        Recebe o nome do projeto da qual deseja encontrar o ID
            :return:                    Retorna uma STR com o nome do projeto referente ao nome passado.
        """
        data = self.__get_all_projects__()
        #
        for project in data['values']:
            if project['name'] == project_name:
                return project['id']
        return None

    def validate(self, status_code: int = None) -> None:
        """
            Funcao que valida o status_code das requisicoes
            :param id:              Recebe o id do objeto
            :param status_code:     Recebe o status code de um objeto request
            :param name:            Recebe o conteudo do objeto
            :return:                Retorna Nada.
        """
        if status_code == 200:
            return True
        elif status_code == 400:
            print('erro de operação (codigo: {0}). Verifique se o projeto existe no stash, '
                  'https://stash.pontoslivelo.com.br/projects'.format(status_code))
            sys.exit(1)
        else:
            print('erro. Servidor indisponivel, verifique o status da rede.(codigo: {0})'.format(status_code))
            sys.exit(1)
        pass

    def analise_content(self, response: requests = None, data: dict = None) -> None:
        """
            Funcao para debug das funcoes
            :param data:        Recebe o conteudo/payload/parameters da chamada
            :param response:    Recebe o response
            :return:            Nada
        """
        print("Data gathered:")
        print("- Data: {0}".format(str(data)))
        if development_control:
            print("- Request URL: {0}".format(response.url))
        print("- Response:")
        print("\t- Code: {0}".format(response.status_code))
        print("\t- Content: {0}".format(str(response.content)))
