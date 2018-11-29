# Library imports
import os
import sys
import yaml
import getopt

# Internal imports
from automation.Help import Help
from automation.Automation import Automation
from automation.FoldersPlus import FoldersPlus
from automation.JenkinsCore import JenkinsCore
from automation.RoleStrategy import RoleStrategy

# =============================================================================================== #
#                                           Função
# =============================================================================================== #
development = False


def validateFields(conteudo: dict = None) -> bool:
    if 'create' in conteudo['acao']:
        if 'project' in conteudo['dado'] and conteudo.get('name'):
            return True
        elif 'role' in conteudo['dado'] and conteudo.get('type') and conteudo.get('name') and conteudo.get('pattern'):
            return True
        else:
            return False

    elif 'delete' in conteudo['acao']:
        if 'project' in conteudo['dado'] and conteudo.get('name'):
            return True
        elif 'role' in conteudo['dado'] and conteudo.get('type') and conteudo.get('name'):
            return True
        else:
            return False

    elif 'get' in conteudo['acao']:
        if conteudo.get('type') and conteudo.get('name'):
            return True
        else:
            return False
    else:
        return False


def automate():
    # Controle interno
    debug = False
    action = dict()

    # Carrega configurações internas
    # Permite carregamento de diferentes configurações (ENV ou ETC ou DEFAULT/INTERNO)
    if os.environ.get('JENKINS_AUTOMATION_CONFIG'):
        config = yaml.load(open(os.environ.get('JENKINS_AUTOMATION_CONFIG')))['projects']
    elif os.path.isfile('/etc/jenkins_automations/config.yaml'):
        config = yaml.load(open('/etc/jenkins_automations/config.yaml'))['projects']
    else:
        # Funcionará apenas apos realizar o build do modulo.
        # Em desenvolvimento, use: 'resources/config.yaml'
        if development:
            config = yaml.load(open('resources/config.yaml'))['projects']
        else:
            config = yaml.load(open('automation/resources/config.yaml'))['projects']
    #

    # Adiciona padrao
    action.setdefault('overwrite', False)

    try:
        # Em casos de execução sem parametros
        if len(sys.argv) <= 1:
            Help()
            sys.exit(0)

        # Coleta acao
        extended_options = ['create=', 'delete=', 'type=', 'name=', 'pattern=', 'overwrite=', 'help', 'debug']
        options, args = getopt.getopt(sys.argv[1:], 'cd:tnp:oh', extended_options)

        # Processa acao
        for opt, value in options:
            # Processa acao principal
            if opt in ['-c', '--create']:
                action['acao'] = 'create'
                action['dado'] = value
            elif opt in ['-d', '--delete']:
                action['acao'] = 'delete'
                action['dado'] = value
            elif opt in ['-g', '--get']:
                action['acao'] = 'get'
                action['dado'] = value
            elif opt in ['-h', '--help']:
                Help()
                sys.exit(0)
            elif opt in ['--debug']:
                debug = True
            else:
                # Processa dados secundarios
                if opt in ['-t', '--type']:
                    action['type'] = value
                elif opt in ['-n', '--name']:
                    action['name'] = value
                elif opt in ['-p', '--pattern']:
                    action['pattern'] = value
                elif opt in ['-o', '--overwrite']:
                    action['overwrite'] = True
                else:
                    continue
    except (getopt.GetoptError, ValueError, KeyError, IndexError) as error:
        raise error

    # Validaçao de dados
    if not validateFields(conteudo=action):
        print("Erro: Parametros invalidos ou falta parametros requisitos para acao desejada.")
        print("Argumentos: {0}".format(str(options)))
        Help()
        sys.exit(1)

    #
    if debug:
        print("Debug: enabled.")
        print("- Action: {0} {1} {2}\n\n".format(action['acao'], action['dado'], action['name']))

    # Cria instancias
    jnk = JenkinsCore()
    role = RoleStrategy(jenkins=jnk, debug=debug)
    folders = FoldersPlus(jenkins=jnk, configuration=config['folder_structure'], debug=debug)
    auto = Automation(role_manager=role, configuration=config['role_strategy'], debug=debug)

    # Realiza procedimento de automacao
    if 'create' in action['acao']:
        if 'project' in action['dado']:
            folders.create_project_structure(project=action['name'])
            auto.create_project_roles(project=action['name'])
        else:
            auto.create_role(data=action)
    elif 'delete' in action['acao']:
        if 'project' in action['dado']:
            folders.delete_project_structure(project=action['name'])
            auto.delete_project_roles(project=action['name'])
        else:
            auto.delete_role(data=action)
    elif 'get' in action['acao']:
        pass
    else:
        pass
    #

    print('Concluido!')
    sys.exit(0)


# =============================================================================================== #
#                                           Inicialização
# =============================================================================================== #
automate()
