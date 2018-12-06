#
import os
import requests

from automation.JenkinsCore import JenkinsCore


class JobManager:

    def __init__(self, jenkins: JenkinsCore = None, debug: bool = None):
        self.debug = debug
        self.jenkins = jenkins
        self.bUrl = 'http://{0}@{1}/job/projects'.format(self.jenkins.get_bAuth(), self.jenkins.get_url())

        # Carrega configurações internas
        # Permite carregamento de diferentes configurações (ENV ou ETC ou DEFAULT/INTERNO)
        if os.environ.get('JENKINS_AUTOMATION_JOB_CONFIG'):
            self.job_configuration = open(os.environ.get('JENKINS_AUTOMATION_JOB_CONFIG'))
        elif os.path.isfile('/etc/jenkins_automations/job_config.xml'):
            self.job_configuration = open('/etc/jenkins_automations/job_config.xml')
        else:
            if os.path.isfile('resources/config.yaml'):
                self.job_configuration = open('resources/config.yaml')
            else:
                self.job_configuration = open('automation/resources/config.yaml')
        pass

    def create_job(self, projeto: str = None, ambiente: str = None, repositorio: str = None):
        # Core
        header = {"Content-Type": "text/xml"}

        name = repositorio.split('/')[-1].split('.',1)[0]
        path = "{0}/job/{1}/job/deploy/job/{2}/createItem?name={3}".format(self.bUrl, projeto, ambiente, name)

        with open('resources/job_config.xml') as xml:
            response = requests.post(url=path, headers=header, data=xml.read())
            print(response)
        pass



    def delete_job(self, project, repository):
        pass
