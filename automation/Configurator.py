#
import os
import yaml


class Configurator:

    def __init__(self):
        # Variaveis de ambiente de controle
        self.global_environment_path = 'JENKINS_AUTOMATION_CONFIGURATION_PATH'
        self.global_job_environment_path = 'JENKINS_AUTOMATION_JOB_CONFIGURATION_PATH'
        self.global_project_environment_path = 'JENKINS_AUTOMATION_PROJECT_CONFIGURATION_PATH'

        # Caminhos padroes de arquivos de configuracao
        self.default_path_configuration = '/etc/jenkins_automations/config.yaml'
        self.default_job_path_configuration = '/etc/jenkins_automations/job_config.xml'
        self.default_project_path_configuration = '/etc/jenkins_automations/project_config.xml'
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

    def load_job_config(self) -> str:
        if os.environ.get(self.global_job_environment_path):
            return open(os.environ.get(self.global_job_environment_path)).read()
        elif os.path.isfile(self.default_job_path_configuration):
            return open(self.default_job_path_configuration).read()
        else:
            # Internal load
            if os.path.isfile('resources/job_config.xml'):
                return open('resources/job_config.xml').read()
            else:
                return open('automation/resources/job_config.xml').read()
        pass

    def load_project_config(self) -> str:
        if os.environ.get(self.global_project_environment_path):
            return open(os.environ.get(self.global_project_environment_path)).read()
        elif os.path.isfile(self.default_project_path_configuration):
            return open(self.default_project_path_configuration).read()
        else:
            # Internal load
            if os.path.isfile('resources/project_config.xml'):
                return open('resources/project_config.xml').read()
            else:
                return open('automation/resources/project_config.xml').read()
        pass

    def get_collpased_execution_parameters(self) -> str:
        return 'cdg:rnetpo:hd'

    def get_expanded_execution_parameters(self) -> list:
        return [
            'create=',
            'delete=',
            'repository=',
            'name=',
            'environment=',
            'type=',
            'pattern=',
            'overwrite=',
            'help',
            'debug'
        ]

    def validate_runtime_options(self, conteudo: dict = None) -> bool:
        if 'create' in conteudo['acao']:
            if 'project' in conteudo['dado'] and conteudo.get('name'):
                return True
            elif 'role' in conteudo['dado'] and conteudo.get('type') and conteudo.get('name') and conteudo.get(
                    'pattern'):
                return True
            elif 'job' in conteudo['dado'] and conteudo.get('name') and conteudo.get('repo'):
                return True
            else:
                return False

        elif 'delete' in conteudo['acao']:
            if 'project' in conteudo['dado'] and conteudo.get('name'):
                return True
            elif 'role' in conteudo['dado'] and conteudo.get('type') and conteudo.get('name'):
                return True
            elif 'job' in conteudo['dado'] and conteudo.get('name') and conteudo.get('repo'):
                return True
            else:
                return False

        elif 'get' in conteudo['acao']:
            if conteudo.get('type') and conteudo.get('name'):
                return True
            else:
                return False
        else:
            return False
