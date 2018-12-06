import requests

# Importa todos os modulos
from automation import *


class Automation:
    def __init__(self, jenkins: JenkinsCore = None, role: RoleStrategy = None, config: dict = None, folder: FoldersPlus = None, job: JobManager = None, debug=False):
        """
            Construtor
            :param jenkins:         Recebe uma instancia do jenkins
            :param role:            Recebe uma instancia das roles
            :param config:          Recebe uma instancia das configuracoes
            :param folder:          Recebe uma instancia de estruturas
            :param job:             Recebe uma instancia de jobs
            :param debug:           Parametro de definição de debug
        """
        # Core
        self.debug = debug
        self.jenkins = jenkins

        # Gerenciadores
        self.job_manager = job
        self.role_manager = role
        self.config_manger = config
        self.folder_manager = folder

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

    def create_project_roles(self, project: str = None) -> None:
        """
            Funcao para criacao do padrao de roles de um projeto especificado.
            :param project:         Recebe o nome do projeto
            :return:                Retorna Nada
        """

        print('Criando role de view')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(self.config_manger['view_role']['name']).replace('<project>', project),
            pattern=str(self.config_manger['view_role']['pattern']).replace('<project>', project),
            perm=str(self.__format_perms__(self.config_manger['view_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando role de build')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(self.config_manger['build_role']['name']).replace('<project>', project),
            pattern=str(self.config_manger['build_role']['pattern']).replace('<project>', project),
            perm=str(self.__format_perms__(self.config_manger['build_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando role de testes')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(self.config_manger['tests_role']['name']).replace('<project>', project),
            pattern=str(self.config_manger['tests_role']['pattern']).replace('<project>', project),
            perm=str(self.__format_perms__(self.config_manger['tests_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando roles de deploy (1/2)')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(self.config_manger['deploy_role']['name']).replace('<project>', project),
            pattern=str(self.config_manger['deploy_role']['pattern']).replace('<project>', project),
            perm=str(self.__format_perms__(self.config_manger['deploy_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando roles de deploy (2/2)')
        for env in self.role_manager.environments:
            self.role_manager.create_role(
                type='projectRoles',
                name=str(self.config_manger['deploy_role_env']['name']).replace('<project>', project).replace('<env>', env),
                pattern=str(self.config_manger['deploy_role_env']['pattern']).replace('<project>', project).replace('<env>',
                                                                                                             env),
                perm=str(self.__format_perms__(self.config_manger['deploy_role_env']['permissionsIds'])),
                overwrite=True
            )
        # End of function

    def delete_project_roles(self, project: str = None) -> None:
        """
            Funcao para remocao das roles padroes de um projeto especificado
            :param project:     Recebe o nome do projeto
            :return:            Retorna Nada
        """

        # Dynamic project roles name list generation (don't blame me)
        role_list = []
        for item in list(self.config_manger.keys()):
            if 'env' not in self.config_manger[item]['name']:
                role_list.append(str(self.config_manger[item]['name']).replace('<project>', project))
            else:
                for env in self.role_manager.environments:
                    role_list.append(str(self.config_manger[item]['name']).replace('<project>', project).replace('<env>', env))
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
        header = {"Content-Type": "text/xml"}

        # Carrega configurações de job
        global_config = Configurator()
        xml = global_config.load_job_config()

        # Controle
        name = repositorio.split('/')[-1].split('.', 1)[0]
        path = "{0}/job/{1}/job/deploy/job/<env>/createItem?name={2}".format(self.jenkins.getBUrl(), projeto, name)

        #
        for env in self.jenkins.getEnvironments():
            print("Criando job de deploy {0} para {1}...".format(name, env), end='')
            response = requests.post(url=path.replace('<env>', env), headers=header, data=xml)
            if response.status_code in [200, 201]:
                print('concluido com sucesso!')
            else:
                print("falhou...(codigo: {0})".format(response.status_code))
            pass
        pass

    def delete_deploy_jobs(self, projeto: str = None, repositorio: str = None) -> None:
        pass

    def create_project_structure(self, project: str = None) -> None:
        # Leitura de configurações
        config = Configurator()
        structure = config.load_config()['folder_structure']
        folder_list = [item.replace('<project>', project) for item in structure]

        # Itera lista e cria pastas
        for folder in folder_list:
            if '<env>' not in folder:
                print('Criando pasta: {0}...'.format(folder.split('/')[-1]), end='')
            #
            if len(folder.split('/')) < 2:
                bUrl = '{0}/createItem'.format(self.jenkins.get_bUrl())
                name = str(folder.split('/')[-1])
                status = self.folder_manager.create_structure(path=bUrl, name=name)
                self.folder_manager.validate(status_code=status.status_code, folder=folder)

            elif len(folder.split('/')) < 3:
                name = str(folder.split('/')[-1])
                bUrl = '{0}/job/{1}/createItem'.format(self.jenkins.get_bUrl(), folder.split('/')[0])
                status = self.folder_manager.create_structure(path=bUrl, name=name)
                self.folder_manager.validate(status_code=status.status_code, folder=folder)

            elif len(folder.split('/')) < 4:
                bUrl = self.jenkins.get_bUrl()
                for item in folder.split('/')[:2]:
                    bUrl += '/job/{0}'.format(item)
                bUrl += '/createItem'

                if '<env>' in folder.split('/')[-1]:
                    for env in self.jenkins.getEnvironments():
                        print('Criando pasta: {0}...'.format(folder.split('/')[-1].replace('<env>', env)), end='')
                        name = str(folder.split('/')[-1]).replace('<env>', env)
                        status = self.folder_manager.create_structure(path=bUrl, name=name)
                        self.folder_manager.validate(status_code=status.status_code, folder=folder, env= env)
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
        pass

    # ================================================================================================================ #
    #                                     Funcoes de interfaciamento                                                   #
    # ================================================================================================================ #

    def create_role(self, data: dict = None) -> None:
        """
            Interface do metodo create da RoleStrategy, que recebe um dict e formata para o metodo da RoleStrategy.
            :param data:        Recebe um dicionario
            :return:            Retorna nada
        """
        self.role_manager.create_role(
            type=data['type'],
            name=data['name'],
            pattern=data['pattern'],
            perm=str(self.__format_perms__(self.config['view_role']['permissionsIds'])),
            overwrite=data['overwrite']
        )
        pass

    def delete_role(self, data: dict = None) -> None:
        """
            Interface do metodo delete da RoleStrategy, que recebe um dit e formata para o metodo da RoleStrategy
            :param data:        Recebe um dicionario
            :return:            Retorna nada
        """
        self.role_manager.delete_role(type=data['type'], name_list=data['name'])
