# Library imports
import requests

# Internal imports
from automation.JenkinsCore import JenkinsCore

# Control
debug = True
development = True


class RoleStrategy:

    def __init__(self, jenkins: JenkinsCore):
        # Retrieve jenkins
        self.jenkins = jenkins

        # Core
        self.bUrl = 'http://{0}@{1}/role-strategy/strategy'.format(self.jenkins.get_bAuth(), self.jenkins.get_url())

        # Controle de ambientes
        self.env_list = ['dev', 'sit', 'uat', 'prd']

        if debug:
            print("Debugging mode:")
            print("- Requests send to: {0}".format(self.bUrl))
            print("- Environments are: {0}".format(str(self.env_list)))

    def get_role(self, type: str = None, name: str = None):
        data = dict(type=type, roleName=name)
        response = requests.post(url='{0}/getRole'.format(self.bUrl), params=data)
        return response

    def get_all_roles(self, type: str = None):
        data = dict(type=type)
        response = requests.post(url='{0}/getAllRoles'.format(self.bUrl), params=data)
        return response

    def create_role(self, type: str = None, name: str = None, pattern: str = None, perm: str = None, overwrite: bool = False):
        data = dict(type=type, roleName=name, pattern=pattern, permissionIds=perm, overwrite=overwrite)
        response = requests.post(url='{0}/addRole'.format(self.bUrl), params=data)
        if development:
            print("Debugging:")
            print("- Data: {0}".format(str(data)))
            print("- requests: {0}".format(response.url))
            print("- response: \n\t\t- Code: {0}\n\t\t- Content: {1}".format(str(response.status_code),
                                                                             str(response.content)))
        return response

    def delete_role(self, type: str = None, name_list: list = None):
        data = dict(type=type, roleNames=name_list)
        response = requests.post(url='{0}/removeRoles'.format(self.bUrl), params=data)
        return response

    def assing_role(self):
        pass

    def unassing_role(self):
        pass

    def create_project_roles(self, project: str = None):
        # Instancia de permissoes
        role_permissions = Permissions()

        print('Criando role de view')
        self.create_role(
            type='projectRoles',
            name='{0} - view'.format(project),
            pattern='^projects(|/{0})'.format(project),
            perm=role_permissions.view_permissions(),
            overwrite=True
        )

        print('Criando role de build')
        self.create_role(
            type='projectRoles',
            name='{0} - build'.format(project),
            pattern='^projects(|/{0}+(|/build+(.*|/docker(|/.*))))'.format(project),
            perm=role_permissions.build_permissions(),
            overwrite=True
        )

        print('Criando role de testes')
        self.create_role(
            type='projectRoles',
            name='{0} - tests'.format(project),
            pattern='^projects(|/{0}+(|/testes(|/.*)))'.format(project),
            perm=role_permissions.tester_permissions(),
            overwrite=True
        )

        print('Criando roles de deploy (1/2)')
        self.create_role(
            type='projectRoles',
            name='{0} - deploy'.format(project),
            pattern='^projects(|/{0}+(|/deploy(|/.*)))'.format(project),
            perm=role_permissions.deploy_permissions(),
            overwrite=True
        )

        print('Criando roles de deploy (2/2)')
        for env in self.env_list:
            self.create_role(
                type='projectRoles',
                name='{0} - deploy {1}'.format(project, env),
                pattern='^projects(|/{0}+(|/deploy+(|/{1}(|/.*))))'.format(project, env),
                perm=role_permissions.deploy_permissions(),
                overwrite=True
            )
        return 0

    def delete_project_roles(self, project: str = None):
        # Dynamic project roles generation (don't blame me)
        role_list = ['{0} - {1}'.format(project, item) for item in ['View', 'Build', 'Test', 'Deploy']]
        role_list += ['{0} - Deploy {1}'.format(project, item) for item in self.env_list]

        #
        response = self.delete_role(type='projectRoles', name_list=role_list)
        return response.status_code


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
        # Define permissoes padroes para todas as roles
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
        # Controle
        data = ''
        for index, item in enumerate(permissions):
            if index < len(permissions):
                data += '{0},'.format(item)
            else:
                data += '{0}'.format(item)
            continue
        #
        return data

    def view_permissions(self):
        return self.format_permissions(self.base_permissions)

    def build_permissions(self):
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
