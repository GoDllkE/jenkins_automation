#
import os
import yaml


class Configurator:

    def __init__(self):
        # Variaveis de ambiente de controle
        self.global_environment_path = 'JENKINS_AUTOMATION_CONFIGURATION_PATH'
        self.global_job_environment_path = 'JENKINS_AUTOMATION_JOB_CONFIGURATION_PATH'

        # Caminhos padroes de arquivos de configuracao
        self.default_path_configuration = '/etc/jenkins_automations/config.yaml'
        self.default_job_path_configuration = '/etc/jenkins_automations/job_config.xml'
        pass

    def load_config(self) -> dict:
        if os.environ.get(self.global_environment_path):
            return yaml.load(open(os.environ.get(self.global_environment_path)))['projects']
        elif os.path.isfile(self.default_path_configuration):
            return yaml.load(open(self.default_path_configuration))['projects']
        else:
            # Internal load
            if os.path.isfile('resources/config.yaml'):
                return yaml.load(open('resources/config.yaml'))['projects']
            else:
                return yaml.load(open('automation/resources/config.yaml'))['projects']
        pass

    def load_job_config(self) -> dict:
        if os.environ.get(self.global_job_environment_path):
            return open(os.environ.get(self.global_job_environment_path)).read()
        elif os.path.isfile(self.default_job_path_configuration):
            return open(self.default_job_path_configuration).read()
        else:
            # Internal load
            if os.path.isfile('resources/config.yaml'):
                return open('resources/config.yaml').read()
            else:
                return open('automation/resources/config.yaml').read()
        pass
