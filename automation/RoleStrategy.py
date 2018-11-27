# Library imports
import requests

# Internal imports
from automation.JenkinsCore import JenkinsCore

# =============================================================================================== #
#                                           Controle
# =============================================================================================== #
debug = True

# =============================================================================================== #
#                                           Classes
# =============================================================================================== #


class RoleStrategy:
    """
        Classe de mapeamento da API do plugin role-strategy
    """
    def __init__(self, jenkins: JenkinsCore):
        """
            Metodo construtor
            :param jenkins:     Recebe uma instancia da classe JenkinsCore
        """
        self.jenkins = jenkins
        self.environments = self.jenkins.getEnvironments()
        self.bUrl = 'http://{0}@{1}/role-strategy/strategy'.format(self.jenkins.get_bAuth(), self.jenkins.get_url())

    def get_role(self, type: str = None, name: str = None) -> requests:
        """
            Funcao para retornar uma role especifica de um tipo especifico
            :param type:        Recebe o tipo de role
            :param name:        Recebe o nome da role
            :return:            Retorna objeto response
        """
        data = dict(type=type, roleName=name)
        response = requests.post(url='{0}/getRole'.format(self.bUrl), params=data)
        return response

    def get_all_roles(self, type: str = None) -> requests:
        """
            Funcao para buscar todas as roles de um tipo especifico
            :param type:        Recebe o tipo da role
            :return:            Retorna objeto response
        """
        data = dict(type=type)
        response = requests.post(url='{0}/getAllRoles'.format(self.bUrl), params=data)
        return response

    def create_role(self, type: str = None, name: str = None, pattern: str = None, perm: str = None,
                    overwrite: bool = False) -> requests:
        """
            Funcao para criacao das roles
            :param type:        Recebe o tipo da role
            :param name:        Recebe o nome da role
            :param pattern:     Recebe o padrao da role
            :param perm:        Recebe as permissoes da role
            :param overwrite:   Opcao para sobrescrever role caso ja exista
            :return:            Retorna objeto response
        """
        data = dict(type=type, roleName=name, pattern=pattern, permissionIds=perm, overwrite=overwrite)
        response = requests.post(url='{0}/addRole'.format(self.bUrl), params=data)
        return response

    def delete_role(self, type: str = None, name_list: str = None) -> requests:
        """
            Funcao para remocao da(s) role(s)
            :param type:        Recebe o tipo da(s) role(s)
            :param name_list:   Recebe uma lista de role(s) (convertido para string - Compatibilidade)
            :return:            Retorna objeto response
        """
        data = dict(type=type, roleNames=name_list)
        response = requests.post(url='{0}/removeRoles'.format(self.bUrl), params=data)
        if debug:
            self.analise_content(data=data, response=response)
        return response

    def assing_role(self):
        pass

    def unassing_role(self):
        pass

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

# =============================================================================================== #


class Permissions:
    """
        Classe para definição das permissoes de acordo com um padrão de role.
        Essa classe define agrupamentos de permissoes com o intuito de se utilizar em roles
        pré-definidas na classe 'RoleStrategy'. Isto é, para cada nova role padrão de projetos, deve-se
        adicionar uma 'função' com as permissoes desejadas para a role.

        Tipos de permissões:
        - hudson.model.Hudson:                                      Permissões gerais do Jenkins (Administer ou Read)
        - hudson.model.Item:                                        Permissões para Jobs
        - hudson.model.View:                                        Permissões para View
        - hudson.model.Run:                                         Permissões para Execução
        - hudson.model.Computer:                                    Permissões referente a agentes
        - hudson.scm.SCM:                                           Permissões para SCM (Tag apenas)
        - com.cloudbees.plugins.credentials.CredentialsProvider:    Permissões para credenciais (Não testado)
    """

    def __init__(self):
        """
            Funcao construtor.
            Define permissoes basicas para todas as roles.
        """
        self.base_permissions = [
            'hudson.model.View.Configure',
            'hudson.model.View.Create',
            'hudson.model.View.Delete',
            'hudson.model.View.Read',
            'hudson.model.Hudson.Read',
            'hudson.model.Item.Discover',
            'hudson.model.Item.Workspace',
            'hudson.model.Item.Read'
        ]

    def format_permissions(self, permissions: list = None) -> str:
        """
            Funcao responsavel pela conversao de dados (compatibilidade)
            :param permissions:     Recebe a lista de permissoes
            :return:                Retorna a lista em string, no modo de compatibilidade
        """
        data = ''
        for index, item in enumerate(permissions):
            if index < (len(permissions)-1):
                data += '{0},'.format(item)
            else:
                data += '{0}'.format(item)
            continue
        #
        return data

    def view_permissions(self):
        """
            Funcao para definir padrao de permissoes para role de visualizacao
            :return:        Retorna lista no modo de compatibilidade
        """
        return self.format_permissions(self.base_permissions)

    def build_permissions(self):
        """
            Funcao para definir padrao de permissoes para role de build
            :return:        Retorna lista no modo de compatibilidade
        """
        return self.format_permissions(self.base_permissions + \
               [
                   'hudson.model.Item.Build',
                   'hudson.model.Item.Cancel',
                   'hudson.model.Item.Configure',
                   'hudson.model.Item.Create',
                   'hudson.model.Item.Delete',
                   'hudson.scm.SCM.Tag',
                   'hudson.model.Run.Artifacts',
                   'hudson.model.Run.Replay',
                   'hudson.model.Run.Update'
               ]
           )

    def deploy_permissions(self):
        """
            Funcao para definir padrao de permissoes para role de deploy
            :return:        Retorna lista no modo de compatibilidade
        """
        return self.format_permissions(self.base_permissions + \
               [
                   'hudson.model.Item.Build',
                   'hudson.model.Item.Cancel',
                   'hudson.model.Run.Artifacts',
                   'hudson.model.Run.Replay',
                   'hudson.model.Run.Update',
                   'hudson.scm.SCM.Tag'
               ]
           )

    def tester_permissions(self):
        """
            Funcao para definir padrao de permissoes para role de teste
            :return:        Retorna lista no modo de compatibilidade
        """
        return self.format_permissions(self.base_permissions + \
               [
                   'hudson.model.Item.Build',
                   'hudson.model.Item.Cancel',
                   'hudson.model.Item.Configure',
                   'hudson.model.Item.Create',
                   'hudson.model.Item.Delete',
                   'hudson.model.Item.Read',
                   'hudson.scm.SCM.Tag',
                   'hudson.model.Run.Artifacts',
                   'hudson.model.Run.Replay',
                   'hudson.model.Run.Update'
               ]
           )

# =============================================================================================== #


class Automation:
    def __init__(self, role_manager: RoleStrategy = None):
        """
            Classe da automacao, responsavel pelas tarefas da automacao.
            :param role_manager:        Recebe uma instancia de uma RoleStrategy
        """
        self.role_manager = role_manager

    def create_project_roles(self, project: str = None) -> None:
        """
            Funcao para criacao do padrao de roles de um projeto especificado.
            :param project:         Recebe o nome do projeto
            :return:                Retorna Nada
        """
        role_permissions = Permissions()

        print('Criando role de view')
        self.role_manager.create_role(
            type='projectRoles',
            name='{0} - view'.format(project),
            pattern='^projects(|/{0})'.format(project),
            perm=role_permissions.view_permissions(),
            overwrite=True
        )

        print('Criando role de build')
        self.role_manager.create_role(
            type='projectRoles',
            name='{0} - build'.format(project),
            pattern='^projects(|/{0}+(|/build+(.*|/docker(|/.*))))'.format(project),
            perm=role_permissions.build_permissions(),
            overwrite=True
        )

        print('Criando role de testes')
        self.role_manager.create_role(
            type='projectRoles',
            name='{0} - tests'.format(project),
            pattern='^projects(|/{0}+(|/testes(|/.*)))'.format(project),
            perm=role_permissions.tester_permissions(),
            overwrite=True
        )

        print('Criando roles de deploy (1/2)')
        self.role_manager.create_role(
            type='projectRoles',
            name='{0} - deploy'.format(project),
            pattern='^projects(|/{0}+(|/deploy(|/.*)))'.format(project),
            perm=role_permissions.deploy_permissions(),
            overwrite=True
        )

        print('Criando roles de deploy (2/2)')
        for env in self.role_manager.environments:
            self.role_manager.create_role(
                type='projectRoles',
                name='{0} - deploy {1}'.format(project, env),
                pattern='^projects(|/{0}+(|/deploy+(|/{1}(|/.*))))'.format(project, env),
                perm=role_permissions.deploy_permissions(),
                overwrite=True
            )
        # End of function

    def delete_project_roles(self, project: str = None) -> None:
        """
            Funcao para remocao das roles padroes de um projeto especificado
            :param project:     Recebe o nome do projeto
            :return:            Retorna Nada
        """
        # Abre instancias
        perm = Permissions()

        # Dynamic project roles generation (don't blame me)
        role_list = ['{0} - {1}'.format(project, item) for item in ['view', 'build', 'tests', 'deploy']]
        role_list += ['{0} - deploy {1}'.format(project, item) for item in self.role_manager.environments]

        #
        self.role_manager.delete_role(type='projectRoles', name_list=perm.format_permissions(role_list))
        # End of function

    def create_role(self, data: dict=None) -> None:
        """
            Interface do metodo create da RoleStrategy, que recebe um dict e formata para o metodo da RoleStrategy.
            :param data:        Recebe um dicionario
            :return:            Retorna nada
        """
        # Abre instancia
        perm = Permissions()

        #
        self.role_manager.create_role(
            type=data['type'],
            name=data['name'],
            pattern=data['pattern'],
            perm=perm.base_permissions,
            overwrite=data['overwrite']
        )
        pass

    def delete_role(self, data: dict=None) -> None:
        """
            Interface do metodo delete da RoleStrategy, que recebe um dit e formata para o metodo da RoleStrategy
            :param data:        Recebe um dicionario
            :return:            Retorna nada
        """
        # Abre instancia
        perm = Permissions()
        self.role_manager.delete_role(type=data['type'], name_list=data['name'])

# =============================================================================================== #
