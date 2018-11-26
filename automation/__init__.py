# Library imports
import sys
import requests

# Internal imports
from automation.JenkinsCore import JenkinsCore
from automation.RoleStrategy import RoleStrategy
from automation.FoldersPlus import FoldersPlus

# Controle de execucao
debug = True


def automate():
    # Recolhe projeto
    if len(sys.argv) == 2:
        project_name = sys.argv[1]
    else:
        if debug:
            project_name = 'teste'
        else:
            print('Erro: nome do projeto nao especificado')
            sys.exit(1)
    #

    # Cria instancias
    jnk = JenkinsCore(url='jenkins-central.pontoslivelo.com.br')
    role = RoleStrategy(jenkins=jnk)

    # Cria roles
    # response = role.delete_project_roles(project=project_name)
    response = role.create_project_roles(project=project_name)
    if debug:
        print("Retorno: {0}".format(str(response)))
    print('Concluido!')

    sys.exit(0)


# Run it
automate()