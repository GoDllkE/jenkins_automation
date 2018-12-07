#
import os
import requests

from automation.JenkinsCore import JenkinsCore


class JobManager:

    def __init__(self, jenkins: JenkinsCore, configuration: str = None, debug: bool = None):
        # Core
        self.debug = debug
        self.jenkins = jenkins
        self.job_configuration = configuration
        self.b_url = b_url = 'http://{0}@{1}/job/projects'.format(self.jenkins.get_bauth(), self.jenkins.get_url())

    def create_job(self, projeto: str = None, caminho: str = None, repositorio: str = None) -> requests:
        # Core
        header = {"Content-Type": "text/xml"}

        name = repositorio.split('/')[-1].split('.', 1)[0]
        path = "{0}{1}/createItem?name={2}".format(self.b_url, caminho, name)

        response = requests.post(url=path, headers=header, data=self.job_configuration)
        if self.debug:
            self.analise_content(response=response, data=dict(headers=header, name=name, config=self.job_configuration))
        return response

    def delete_job(self, caminho: str = None, repositorio: str = None) -> requests:
        # Core
        name = repositorio.split('/')[-1].split('.', 1)[0]
        #
        path = "{0}{1}/job/{2}/doDelete".format(self.b_url, caminho, name)
        response = requests.post(url=path)
        if self.debug:
            self.analise_content(response=response, data={})
        return response


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
        print("\nData gathered:")
        print("- Data: {0}".format(str(data)))
        print("- Request URL: {0}".format(response.url))
        print("- Response:")
        print("\t- Code: {0}".format(response.status_code))
        print("\t- Content: {0}".format(str(response.content)))

    def validate(self, status_code: int = None, job: str = None, env: str = None) -> None:
        """
            Funcao que valida o status_code das requisicoes
            :param status_code:     Recebe o status code de um objeto request
            :param job:             Recebe o name do objeto que foi requisitado a ser criado
            :param env:             (Opcional) Recebe nome do ambiente
            :return:                Retorna Nada.
        """
        if status_code == 200:
            print('concluido com sucesso!')
        elif status_code == 400:
            if env:
                print('erro. Job "{0}" ja existe'.format(job.replace('<env>', env)))
            else:
                print('erro. Job "{0}" ja existe'.format(job))
        else:
            if env:
                print('erro. Nao foi possivel criar job "{0}" (codigo: {1})'.format(job.replace('<env>', env), status_code))
            else:
                print('erro. Nao foi possivel criar job "{0}" (codigo: {1})'.format(job, status_code))
        pass

    # ================================================================================================================ #
