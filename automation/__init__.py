# Library imports
import sys
import requests

# Internal imports
from automation.JenkinsCore import JenkinsCore
from automation.RoleStrategy import RoleStrategy
from automation.FoldersPlus import FoldersPlus

# Controle de execucao
debug = True
development = True
default_action = 'create'
default_project = 'teste'


def automate():
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
    jnk = JenkinsCore(url='jenkins-central.pontoslivelo.com.br')
    role = RoleStrategy(jenkins=jnk)

    # Cria roles
    # response = role.delete_project_roles(project=project_name)
    response = role.create_project_roles(project=project)
    if debug:
        print("Retorno: {0}".format(str(response)))
    print('Concluido!')

    sys.exit(0)


# Run it
automate()
