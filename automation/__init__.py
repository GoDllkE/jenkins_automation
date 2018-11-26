# Library imports
import sys
import getopt

# Internal imports
from automation.JenkinsCore import JenkinsCore
from automation.RoleStrategy import RoleStrategy, Automation
from automation.FoldersPlus import FoldersPlus

# =============================================================================================== #
#                                           Controle
# =============================================================================================== #
debug = True
development = True
default_action = 'create'
default_project = 'teste'

# =============================================================================================== #
#                                           Função
# =============================================================================================== #


def automate():
    try:
        options, args = getopt.getopt(sys.argv[1:], 'p:cdr:', ['project', 'create', 'delete', 'remove'])
    except getopt.GetoptError as error:
        raise error

    for opt, value in options:
        if opt in ['-p', '--project']:
            pass
        elif opt in ['-c', '--create']:
            pass
        elif opt in ['-d', '--delete']:
            pass
        else:
            assert False

    if len(sys.argv) == 3:
        action = sys.argv[1]
        project = sys.argv[2]
    else:
        if development:
            action = default_action
            project = default_project
        else:
            print('Erro: ação e nome do projeto nao especificado')
            sys.exit(1)
    #
    if debug:
        print("Using default options for development.")
        print("- Action: {0}: {1}\n\n".format(action, project))

    # Cria instancias
    jnk = JenkinsCore()
    role = RoleStrategy(jenkins=jnk)
    auto = Automation(role_manager=role)

    # Cria roles
    # auto.create_project_roles(project=project)
    # auto.delete_project_roles(project=project)

    print('Concluido!')
    print('Verifique: https://jenkins-central.pontoslivelo.com.br/role-strategy/manage-roles')

    sys.exit(0)


# =============================================================================================== #
#                                           Inicialização
# =============================================================================================== #
automate()
