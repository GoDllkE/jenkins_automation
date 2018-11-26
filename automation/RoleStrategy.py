#
import json
import requests


class RoleStrategy:

    def __init__(self, url: str = None, username: str = None, password: str = None):
        # Core
        self.bAuth = '{0}:{1}'.format(username, password)
        self.bUrl = 'https://{0}@{1}/role-strategy/strategy'.format(self.bAuth, url)

        # Controle de ambientes
        self.env_list = ['dev', 'sit', 'uat', 'prd']
        pass

    def get_role(self, type: str = None, name: str = None):
        data = dict(roleType=type, roleName=name)
        response = requests.post(url='{0}/getRole'.format(self.bUrl), params=data)
        return response

    def get_all_roles(self, type: str = None):
        data = dict(roleType=type)
        response = requests.post(url='{0}/getAllRoles'.format(self.bUrl), params=data)
        return response

    def create_role(self, type: str = None, name: str = None, pattern: str = None, perm: list = None,
                    overwrite: bool = False):
        data = dict(roleType=type, roleName=name, pattern=pattern, permissionsId=perm, overwrite=overwrite)
        response = requests.post(url='{0}/addRole'.format(self.bUrl), params=data)
        return response

    def delete_role(self, type: str = None, name_list: list = None):
        data = dict(roleType=type, roleNames=name_list)
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
            name='{0} - View'.format(project),
            pattern='^projects(|/{0})'.format(project),
            perm=role_permissions.view_permissions(),
            overwrite=True
        )

        print('Criando role de build')
        self.create_role(
            type='projectRoles',
            name='{0} - Build'.format(project),
            pattern='^projects(|/{0}+(|/build+(.*|/docker(|/.*))))'.format(project),
            perm=role_permissions.build_permissions(),
            overwrite=True
        )

        print('Criando role de testes')
        self.create_role(
            type='projectRoles',
            name='{0} - Build'.format(project),
            pattern='^projects(|/{0}+(|/testes(|/.*)))'.format(project),
            perm=role_permissions.tester_permissions(),
            overwrite=True
        )

        print('Criando roles de deploy (1/2)')
        self.create_role(
            type='projectRoles',
            name='{0} - Deploy'.format(project),
            pattern='^projects(|/{0}+(|/deploy(|/.*)))'.format(project),
            perm=role_permissions.deploy_permissions(),
            overwrite=True
        )

        print('Criando roles de deploy (2/2)')
        for env in self.env_list:
            self.create_role(
                type='projectRoles',
                name='{0} - {1}'.format(project, env),
                pattern='^projects(|/{0}+(|/deploy+(|/{1}(|/.*))))'.format(project, env),
                perm=role_permissions.deploy_permissions(),
                overwrite=True
            )
        return 0

    def delete_project_roles(self, project: str = None):
        #
        role_list = ['{0} - {1}'.format(project, item) for item in ['View', 'Build', 'Test', 'Deploy']]
        role_list += ['{0} - Deploy {1}'.format(project, item) for item in self.env_list]
        #
        print("Removendo roles: {0}".format(str(role_list)))
        self.delete_role(type='projectRoles', name_list=role_list)
        return 0


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
            'hudson.model.Hudson.Read',
            'hudson.model.Item.extendedRead',
            'hudson.model.Item.Discover',
            'hudson.model.Item.Workspace'
        ]

    def view_permissions(self):
        return self.base_permissions

    def build_permissions(self):
        return self.base_permissions + \
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

    def deploy_permissions(self):
        return self.base_permissions + \
               [
                   'hudson.model.Run.Artifacts',
                   'hudson.model.Run.Replay',
                   'hudson.model.Run.Update',
                   'hudson.scm.SCM.Tag'
               ]

    def tester_permissions(self):
        return self.base_permissions + \
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