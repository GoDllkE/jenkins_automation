# Library imports
import requests

# Internal imports
from automation import JenkinsCore


class FoldersPlus:

    def __init__(self, jenkins: JenkinsCore, configuration: list = None, debug=False):
        """
        Metodo construtor
        :param debug:
        :param jenkins:         Recebe uma instancia da classe JenkinsCore
        :param configuration    Recebe uma lista da estrutura padrão a seguir.
        """
        # self.debug = debug
        # self.jenkins = jenkins
        # self.structure = configuration
        # self.bUrl = 'http://{0}@{1}/job/projects'.format(self.jenkins.get_bAuth(), self.jenkins.get_url())

    def create_structure(self, path: str = None, name: str = None) -> requests:
        # Controle interno
        header = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"name": "{0}".format(name), "mode": "com.cloudbees.hudson.plugins.folder.Folder", "Submit": "OK"}
        response = requests.post(url=path, headers=header, params=data)
        return response

    def delete_structure(self, path: str = None, name: str = None) -> requests:
        pass

    # def create_project_structure(self, project: str = None) -> None:
    #     # Controle interno
    #     headers = {"Content-Type": "application/x-www-form-urlencoded"}
    #     folder_list = [item.replace('<project>', project) for item in self.structure]
    #     data = {"name": "", "mode": "com.cloudbees.hudson.plugins.folder.Folder", "Submit": "OK"}
    #
    #     # Itera lista e cria pastas
    #     for folder in folder_list:
    #         # Mensagem
    #         if '<env>' not in folder:
    #             print('Criando pasta: {0}...'.format(folder.split('/')[-1]), end='')
    #
    #         #
    #         if len(folder.split('/')) < 2:
    #             bUrl = '{0}/createItem'.format(self.bUrl)
    #             data['name'] = str(folder.split('/')[-1])
    #             response = requests.post(url=bUrl, headers=headers, params=data)
    #             self.validate(status_code=response.status_code, folder=folder)
    #
    #         elif len(folder.split('/')) < 3:
    #             data['name'] = str(folder.split('/')[-1])
    #             bUrl = '{0}/job/{1}/createItem'.format(self.bUrl, folder.split('/')[0])
    #             response = requests.post(url=bUrl, headers=headers, params=data)
    #             self.validate(status_code=response.status_code, folder=folder)
    #
    #         elif len(folder.split('/')) < 4:
    #             # Prepara url
    #             bUrl = self.bUrl
    #             for item in folder.split('/')[:2]:
    #                 bUrl += '/job/{0}'.format(item)
    #             bUrl += '/createItem'
    #
    #             if '<env>' in folder.split('/')[-1]:
    #                 # Itera lista de ambientes
    #                 for env in self.jenkins.getEnvironments():
    #                     print('Criando pasta: {0}...'.format(folder.split('/')[-1].replace('<env>', env)), end='')
    #                     data['name'] = str(folder.split('/')[-1]).replace('<env>', env)
    #                     response = requests.post(url=bUrl, headers=headers, params=data)
    #                     self.validate(status_code=response.status_code, folder=folder, env=env)
    #
    #                 #
    #                 continue
    #             else:
    #                 data['name'] = str(folder.split('/')[-1])
    #                 response = requests.post(url=bUrl, headers=headers, params=data)
    #                 self.validate(status_code=response.status_code, folder=folder)
    #         else:
    #             print("Path too long or to short! ({0}".format(folder))
    #             exit(1)
    #         pass
    #     # End of function
    #
    # def delete_project_structure(self, project: str = None) -> None:
    #     """
    #         Funcao para deletar um conjunto de pastas de um projeto
    #         :param project:         Recebe o nome do projeto
    #         :return:                Retorna nada
    #     """
    #     print('Deletando estrutura de pastas do projeto "{0}"...'.format(project), end='')
    #     bUrl = '{0}/job/{1}/doDelete'.format(self.bUrl, project)
    #     response = requests.post(url=bUrl)
    #     if response.status_code == 200:
    #         print("concluido com sucesso!")
    #     elif response.status_code == 404:
    #         print("erro. A estrutura de pastas nao foi encontrada/nao existe.")
    #     else:
    #         print("erro. Desconhecido (codigo: {0})".format(response.status_code))
    #     pass

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
                print('erro. Pasta "{0}" ja existe'.format(folder.replace('<env>', env)))
            else:
                print('erro. Pasta "{0}" ja existe'.format(folder))
        else:
            if env:
                print('erro. Nao foi possivel criar pasta "{0}" (codigo: {1})'.format(folder.replace('<env>', env),
                                                                                      status_code))
            else:
                print('erro. Nao foi possivel criar pasta "{0}" (codigo: {1})'.format(folder, status_code))
        pass
