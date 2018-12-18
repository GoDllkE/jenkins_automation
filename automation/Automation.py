import sys

import requests

# Importa todos os modulos
from automation.JobManager import JobManager
from automation.JenkinsCore import JenkinsCore
from automation.FoldersPlus import FoldersPlus
from automation.Configurator import Configurator
from automation.RoleStrategy import RoleStrategy


class Automation:

    def __init__(self, jenkins: JenkinsCore = None, configuration: Configurator = None, debug=False):
        """
            Construtor
            :param jenkins:         Recebe uma instancia do jenkins
            :param configuration:   Recebe uma instancia das configuracoes
            :param debug:           Parametro de definição de debug
        """
        # Core
        self.debug = debug
        self.jenkins = jenkins
        self.config_manger = configuration

        # Instancias
        self.role_manager = RoleStrategy(jenkins=self.jenkins, debug=self.debug)
        self.folder_manager = FoldersPlus(jenkins=self.jenkins, debug=self.debug)
        self.job_manager = JobManager(jenkins=self.jenkins, configuration=self.config_manger, debug=self.debug)

    def __format_perms__(self, permissions: list = None) -> str:
        """
            Funcao responsavel pela conversao de dados (compatibilidade)
            :param permissions:     Recebe a lista de permissoes
            :return:                Retorna a lista em string, no modo de compatibilidade
        """
        data = ''
        for index, item in enumerate(permissions):
            if index < (len(permissions) - 1):
                data += '{0},'.format(item)
            else:
                data += '{0}'.format(item)
            continue
        #
        return data

    # ================================================================================================================ #
    #                                       Funcoes de automação                                                       #
    # ================================================================================================================ #

    def create_project_roles(self, project: str = None, project_id: str = None) -> None:
        """
            Funcao para criacao do padrao de roles de um projeto especificado.
            :param project:         Recebe o nome do projeto
            :param project_id:      Recebe o ID do projeto no bitbucket
            :return:                Retorna Nada
        """
        # Core
        if project_id is not None:
            project_id = project_id.upper()
        else:
            project_id = project
        role_config = self.config_manger.load_config()['role_strategy']

        print('Criando role de view')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(role_config['view_role']['name']).replace('<project>', project_id),
            pattern=str(role_config['view_role']['pattern']).replace('<project>', project),
            perm=str(self.__format_perms__(role_config['view_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando role de build')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(role_config['build_role']['name']).replace('<project>', project_id),
            pattern=str(role_config['build_role']['pattern']).replace('<project>', project),
            perm=str(self.__format_perms__(role_config['build_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando role de testes')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(role_config['tests_role']['name']).replace('<project>', project_id),
            pattern=str(role_config['tests_role']['pattern']).replace('<project>', project),
            perm=str(self.__format_perms__(role_config['tests_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando roles de deploy (1/2)')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(role_config['deploy_role']['name']).replace('<project>', project_id),
            pattern=str(role_config['deploy_role']['pattern']).replace('<project>', project),
            perm=str(self.__format_perms__(role_config['deploy_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando roles de deploy (2/2)')
        for env in self.role_manager.environments:
            self.role_manager.create_role(
                type='projectRoles',
                name=str(role_config['deploy_role_env']['name']).replace('<project>', project_id).replace('<env>', env),
                pattern=str(role_config['deploy_role_env']['pattern']).replace('<project>', project).replace('<env>', env),
                perm=str(self.__format_perms__(role_config['deploy_role_env']['permissionsIds'])),
                overwrite=True
            )
        # End of function

    def delete_project_roles(self, project: str = None) -> None:
        """
            Funcao para remocao das roles padroes de um projeto especificado
            :param project:     Recebe o nome do projeto
            :return:            Retorna Nada
        """
        # Core
        role_config = self.config_manger.load_config()['role_strategy']

        # Dynamic project roles name list generation (don't blame me)
        role_list = []
        for item in list(role_config.keys()):
            if 'env' not in role_config[item]['name']:
                role_list.append(str(role_config[item]['name']).replace('<project>', project))
            else:
                for env in self.role_manager.environments:
                    role_list.append(str(role_config[item]['name']).replace('<project>', project).replace('<env>', env))
                continue
            continue
        #

        print("Deletando role(s): {0}...".format(str(role_list)), end='')
        self.role_manager.delete_role(type='projectRoles', name_list=self.__format_perms__(role_list))
        print("concluido!")
        # End of function

    def create_deploy_jobs(self, projeto: str = None, repositorio: str = None) -> None:
        """
            Funcao que cria jobs de deploy dado um projeto e um repositorio em especifico
            :param projeto:                     Nome do projeto a na estrutura do jenkins
            :param repositorio:                 Nome do repositorio da qual deseja criar os jobs de deploy.
            :return:                            Retorna nada
        """
        # Core
        name = repositorio.split('/')[-1].split('.', 1)[0]
        path = "/job/{0}/job/deploy/job/<env>".format(projeto)

        #
        for env in self.jenkins.get_environments():
            # Atualiza job de deploy
            configuration = self.config_manger.load_job_config().replace('#cluster#', "\"{0}\"".format(env))
            configuration = configuration.replace('#git_url#', "\"{0}\"".format(repositorio))

            response = self.job_manager.create_deploy_job(caminho=path.replace('<env>', env),
                                                          configuration=configuration, repositorio=repositorio)
            self.job_manager.validate(status_code=response.status_code, job=name, env=env)
            if response.status_code in [200]:
                print("Criando job de deploy {0} para {1}...".format(name, env), end='')
        #
        pass

    def create_missing_deploy_jobs(self, projeto: str = None, ambiente: list = None, repositorio: str = None) -> None:
        """
            Funcao que cria jobs de deploy dado um projeto e um repositorio em especifico
            :param ambiente:                    Recebe lista de ambientes onde o job esta faltando.
            :param projeto:                     Nome do projeto a na estrutura do jenkins
            :param repositorio:                 Nome do repositorio da qual deseja criar os jobs de deploy.
            :return:                            Retorna nada
        """
        # Core
        name = repositorio.split('/')[-1].split('.', 1)[0]
        path = "/job/{0}/job/deploy/job/<env>".format(projeto, ambiente)

        #
        for env in ambiente:
            # Atualiza job de deploy
            configuration = self.config_manger.load_job_config().replace('#cluster#', "\"{0}\"".format(env))
            configuration = configuration.replace('#git_url#', "\"{0}\"".format(repositorio))

            print("Criando job de deploy {0} para {1}...".format(name, env), end='')
            response = self.job_manager.create_deploy_job(caminho=path.replace('<env>', env),
                                                          configuration=configuration, repositorio=repositorio)
            self.job_manager.validate(status_code=response.status_code, job=name, env=env)

        #
        pass

    def delete_deploy_jobs(self, projeto: str = None, repositorio: str = None) -> None:
        # Controle
        name = repositorio.split('/')[-1].split('.', 1)[0]
        path = "/job/{0}/job/deploy/job/<env>".format(projeto)

        for env in self.jenkins.get_environments():
            print("Deletando job de deploy {0} para {1}...".format(name, env), end='')
            response = self.job_manager.delete_deploy_job(caminho=path.replace('<env>', env), repositorio=repositorio)
            self.job_manager.validate(status_code=response.status_code, job=name, env=env)
        #
        pass

    def create_project_structure(self, project: str = None) -> None:
        # Leitura de configurações
        structure = self.config_manger.load_config()['folder_structure']
        folder_list = [item.replace('<project>', project) for item in structure]

        # Itera lista e cria pastas
        for folder in folder_list:
            if '<env>' not in folder:
                print('Criando pasta: {0}...'.format(folder.split('/')[-1]), end='')
            #
            if len(folder.split('/')) < 2:
                bUrl = '/createItem'.format()
                name = str(folder.split('/')[-1])
                status = self.folder_manager.create_structure(path=bUrl, name=name)
                self.folder_manager.validate(status_code=status.status_code, folder=folder)


            elif len(folder.split('/')) < 3:
                name = str(folder.split('/')[-1])
                bUrl = '/job/{0}/createItem'.format(folder.split('/')[0])
                status = self.folder_manager.create_structure(path=bUrl, name=name)
                self.folder_manager.validate(status_code=status.status_code, folder=folder)

            elif len(folder.split('/')) < 4:
                bUrl = ''
                for item in folder.split('/')[:2]:
                    bUrl += '/job/{0}'.format(item)
                bUrl += '/createItem'

                if '<env>' in folder.split('/')[-1]:
                    for env in self.jenkins.get_environments():
                        print('Criando pasta: {0}...'.format(folder.split('/')[-1].replace('<env>', env)), end='')
                        name = str(folder.split('/')[-1]).replace('<env>', env)
                        status = self.folder_manager.create_structure(path=bUrl, name=name)
                        self.folder_manager.validate(status_code=status.status_code, folder=folder, env=env)
                    #
                    continue
                else:
                    name = str(folder.split('/')[-1])
                    status = self.folder_manager.create_structure(path=bUrl, name=name)
                    self.folder_manager.validate(status_code=status.status_code, folder=folder)

            else:
                print("Path too long or to short! ({0}".format(folder))
                exit(1)
            pass
        # End of function

    def delete_project_structure(self, project: str = None) -> None:
        # Core
        response = self.folder_manager.delete_structure(name=project)
        #
        print("Deletando estrutura do projeto {0}...".format(project), end='')
        self.folder_manager.validate(status_code=response.status_code, folder=project)
        pass

    def import_project_builds(self, project: str = None, project_id: str = None, dados: dict = None):
        # Core
        data = {}
        data.setdefault('project_owner', project_id)

        # Valida se existe credenciais passadas
        if dados.get('credenciais'):
            data.setdefault('credencial', dados.get('credenciais'))
        else:
            data.setdefault('credencial', 'jenkins-user')

        # Valida se existe intervalo customizado
        if dados.get('intervalo'):
            data.setdefault('intervalo', dados.get('intervalo'))
        else:
            data.setdefault('intervalo', 120000)

        print("Importando projeto do stash para o jenkins...", end='')
        response = self.job_manager.import_project_jobs(projeto=project, data=data)
        self.job_manager.validate(status_code=response.status_code, job=project)
        pass

    # ================================================================================================================ #

    def check_imported_folder(self, project: str = None) -> bool:
        # Core
        url = "{0}/jobs/projects/job/{1}/build/api/json".format(self.jenkins.get_burl(), project)

        print("Verificando existencia da importaçao...", end='')
        response = requests.get(url=url)
        if self.debug:
            self.job_manager.analise_content(data={}, response=response)

        # Validação
        if response.status_code in [404]:
            print("não encontrado. (Adicionado a lista de pendentes)")
            return False
        elif response.status_code in [200]:
            print("importação já existe.")
            return True
        else:
            print("erro: desconhecido (codigo: {0})".format(response.status_code))
            sys.exit(1)

    def check_deploy_jobs(self, project: str = None, repositorio: str = None) -> list:
        # Controle
        missing = []
        job_name = repositorio.split('/')[-1].split('.', 1)[0]

        for env in self.jenkins.get_environments():
            #
            # Cria URL de pesquisa
            url = "{0}/job/projects/job/{1}/job/deploy/job/{2}/job/{3}/api/json".format(self.jenkins.get_burl(), project, env, job_name)

            print("Verificando job de deploy do ambiente de {0}...".format(env), end='')
            response = requests.get(url=url)
            if self.debug:
                self.job_manager.analise_content(data={}, response=response)

            # Criando validação
            if response.status_code not in [200]:
                print('não encontrado. (Adicionado a lista de pendentes)')
                missing.append(env)
            else:
                print('encontrado!')
                continue

        #
        return missing

    # ================================================================================================================ #
    #                                     Funcoes de interfaciamento                                                   #
    # ================================================================================================================ #

    def create_role(self, data: dict = None) -> None:
        """
            Interface do metodo create da RoleStrategy, que recebe um dict e formata para o metodo da RoleStrategy.
            :param data:        Recebe um dicionario
            :return:            Retorna nada
        """
        # Core
        role_config = self.config_manger.load_config()['role_strategy']

        self.role_manager.create_role(
            type=data['type'],
            name=data['name'],
            pattern=data['pattern'],
            perm=str(self.__format_perms__(role_config['view_role']['permissionsIds'])),
            overwrite=data['overwrite']
        )

    def delete_role(self, data: dict = None) -> None:
        """
            Interface do metodo delete da RoleStrategy, que recebe um dit e formata para o metodo da RoleStrategy
            :param data:        Recebe um dicionario
            :return:            Retorna nada
        """
        self.role_manager.delete_role(type=data['type'], name_list=data['name'])

    def create_job(self, data: dict = None) -> None:
        pass

    def delete_job(self, data: dict = None) -> None:
        pass

    # ================================================================================================================ #