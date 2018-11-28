#
from automation import JenkinsCore


class FoldersPlus:

    def __init__(self, jenkins: JenkinsCore, configuration: list = None, debug=False):
        """
        Metodo construtor
        :param debug:
        :param jenkins:         Recebe uma instancia da classe JenkinsCore
        :param configuration    Recebe uma lista da estrutura padrão a seguir.
        """
        self.debug = debug
        self.jenkins = jenkins
        self.configuration = configuration
        self.environments = self.jenkins.getEnvironments()
        self.bUrl = 'https://{0}@{1}'.format(self.jenkins.get_bAuth(), self.jenkins.get_url())

    def create_project_structure(self, project: str = None) -> None:
        pass

    def delete_project_structure(self, project: str = None) -> None:
        pass
