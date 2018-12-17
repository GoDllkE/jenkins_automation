#
import os
import yaml


class Configurator:

    def __init__(self):
        """
            Construtor.
            Define variaveis de ambiente de leitura de arquivos de configuração e caminhos padrões para os mesmos.
        """
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
        """
            Funcao de carregamento dinamico das configuração requeridas,
                uma vez definidas no construtor da classe Configurator
            :return:    Retorna dicionario com configuracoes
        """
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
        """
            Funcao de carregamento dinamico das configurações dos jobs de deploy padrão da automação
            :return:    Retorna STR contendo o XML padrão do job de deploy
        """
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
        """
            funcao de carregamento dinamico das configurações da importação de projetos do bitbucket
            :return:    Retorna STR contendo o XML padrão da importação
        """
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
        """
            Função que define sequencia de parametros/opcoes reduzidas do programa
            :return:    Retorna cadeia de caracteres STR na ordem correta.
        """
        return 'cdg:rnietpoukqs:hd'

    def get_expanded_execution_parameters(self) -> list:
        """
            Funcao que define sequencia de parametros/opcoes por extenso do programa.
            :return:    Retorna lista de parametros na ordem correta.
        """
        return [
            'check=', 'create=', 'delete=', 'get=',
            'repo=', 'repository=',
            'name=',
            'id=', 'project_id=', 'project_stash_id=',
            'env=', 'environment=',
            'type=', 'role-type=',
            'regex=', 'pattern=',
            'overwrite=',
            'intervalo=',
            'credential=',
            'help', 'debug'
        ]

    def __validate_field__(self, parameter: str = None, value: str = None) -> bool:
        """
            Funcao da validacao dos valores dos parametros utilizados na inicialização do programa.
            :param parameter:   Recebe um do(s) parametro(s) passado(s)
            :param value:       Recebe o valor do parametro passado
            :return:            Retorna booleano indicado validação
        """
        if value in [None, '']:
            print('Erro: Parametro {0} vazio ou invalido (valor: {1})'.format(parameter, value))
            return False
        else:
            return True

    def validate_runtime_options(self, conteudo: dict = None) -> bool:
        """
            Funcao de validação do conjunto de parametros utilizados em ordem de requerimento das funcionalidades.
            :param conteudo:    Recebe dicionario com o conteudo recebido na incialização
            :return:            Retorna booleano indicando validação.
        """
        if 'create' in conteudo['acao']:
            if 'project' in conteudo['dado']:
                return self.__validate_field__('id', conteudo.get('id'))
            elif 'role' in conteudo['dado']:
                return (self.__validate_field__('type', conteudo.get('type')) and
                        self.__validate_field__('name', conteudo.get('name')) and
                        self.__validate_field__('pattern', conteudo.get('pattern')))
            elif 'deploy_jobs' in conteudo['dado']:
                return (self.__validate_field__('id', conteudo.get('id')) and
                        self.__validate_field__('repo', conteudo.get('repo')))
            else:
                return False

        elif 'delete' in conteudo['acao']:
            if 'project' in conteudo['dado']:
                return self.__validate_field__('id', conteudo.get('id'))
            elif 'role' in conteudo['dado']:
                return (self.__validate_field__('type', conteudo.get('type')) and
                        self.__validate_field__('name', conteudo.get('name')))
            elif 'deploy_jobs' in conteudo['dado']:
                return (self.__validate_field__('id', conteudo.get('id')) and
                        self.__validate_field__('repo', conteudo.get('repo')))
            else:
                return False

        elif 'check' in conteudo['acao']:
            if 'project' in conteudo['dado']:
                return self.__validate_field__('id', conteudo.get('id'))
            elif 'deploy_jobs' in conteudo['dado']:
                return (self.__validate_field__('id', conteudo.get('id')) and
                        self.__validate_field__('repo', conteudo.get('repo')))
            else:
                return False

        elif 'get' in conteudo['acao']:
            if conteudo.get('type') and conteudo.get('name'):
                return (self.__validate_field__('type', conteudo.get('type')) and
                        self.__validate_field__('repo', conteudo.get('name')))
            else:
                return False
        else:
            return False
