from automation import RoleStrategy


class Automation:
    def __init__(self, role_manager: RoleStrategy = None, configuration: dict = None, debug=False):
        """
            Classe da automacao, responsavel pelas tarefas da automacao.
            :param debug:
            :param role_manager:        Recebe uma instancia de uma RoleStrategy
            :param configuration        Recebe um dicionario de roles da automacao.
        """
        self.debug = debug
        self.config = configuration
        self.role_manager = role_manager

    def format_perms(self, permissions: list = None) -> str:
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

    def create_project_roles(self, project: str = None) -> None:
        """
            Funcao para criacao do padrao de roles de um projeto especificado.
            :param project:         Recebe o nome do projeto
            :return:                Retorna Nada
        """

        print('Criando role de view')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(self.config['view_role']['name']).replace('<project>', project),
            pattern=str(self.config['view_role']['pattern']).replace('<project>', project),
            perm=str(self.format_perms(self.config['view_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando role de build')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(self.config['build_role']['name']).replace('<project>', project),
            pattern=str(self.config['build_role']['pattern']).replace('<project>', project),
            perm=str(self.format_perms(self.config['build_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando role de testes')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(self.config['tests_role']['name']).replace('<project>', project),
            pattern=str(self.config['tests_role']['pattern']).replace('<project>', project),
            perm=str(self.format_perms(self.config['tests_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando roles de deploy (1/2)')
        self.role_manager.create_role(
            type='projectRoles',
            name=str(self.config['deploy_role']['name']).replace('<project>', project),
            pattern=str(self.config['deploy_role']['pattern']).replace('<project>', project),
            perm=str(self.format_perms(self.config['deploy_role']['permissionsIds'])),
            overwrite=True
        )

        print('Criando roles de deploy (2/2)')
        for env in self.role_manager.environments:
            self.role_manager.create_role(
                type='projectRoles',
                name=str(self.config['deploy_role_env']['name']).replace('<project>', project).replace('<env>', env),
                pattern=str(self.config['deploy_role_env']['pattern']).replace('<project>', project).replace('<env>', env),
                perm=str(self.format_perms(self.config['deploy_role_env']['permissionsIds'])),
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
        for item in list(self.config.keys()):
            if 'env' not in self.config[item]['name']:
                role_list.append(str(self.config[item]['name']).replace('<project>', project))
            else:
                for env in self.role_manager.environments:
                    role_list.append(str(self.config[item]['name']).replace('<project>', project).replace('<env>', env))
                continue
            continue
        #

        print("Deletando role(s): {0}".format(str(role_list)), end='')
        self.role_manager.delete_role(type='projectRoles', name_list=self.format_perms(role_list))
        print("concluido!")
        # End of function

    def create_role(self, data: dict=None) -> None:
        """
            Interface do metodo create da RoleStrategy, que recebe um dict e formata para o metodo da RoleStrategy.
            :param data:        Recebe um dicionario
            :return:            Retorna nada
        """
        self.role_manager.create_role(
            type=data['type'],
            name=data['name'],
            pattern=data['pattern'],
            perm=str(self.format_perms(self.config['view_role']['permissionsIds'])),
            overwrite=data['overwrite']
        )
        pass

    def delete_role(self, data: dict=None) -> None:
        """
            Interface do metodo delete da RoleStrategy, que recebe um dit e formata para o metodo da RoleStrategy
            :param data:        Recebe um dicionario
            :return:            Retorna nada
        """
        self.role_manager.delete_role(type=data['type'], name_list=data['name'])