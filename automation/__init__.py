# Library imports
import sys
import getopt

# Internal imports
from automation.Help import Help
from automation.Automation import Automation
from automation.JenkinsCore import JenkinsCore
from automation.Configurator import Configurator

# =============================================================================================== #
#                                           Main
# =============================================================================================== #


def automate():
    # Controle interno
    debug = False

    # Core
    global_config = Configurator()

    # Adiciona padrao
    action = dict()
    action.setdefault('overwrite', False)

    try:
        # Em casos de execução sem parametros
        if len(sys.argv) <= 1:
            Help()
            sys.exit(0)

        # Coleta acao
        options, args = getopt.getopt(sys.argv[1:], global_config.get_collpased_execution_parameters(),
                                      global_config.get_expanded_execution_parameters())

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
            elif opt in ['--check']:
                action['acao'] = 'check'
                action['dado'] = value
            elif opt in ['--debug']:
                debug = True
            elif opt in ['-h', '--help']:
                Help()
                sys.exit(0)
            else:
                # Processa dados secundarios
                if opt in ['-t', '--type', '--role-type']:
                    action['type'] = value
                elif opt in ['-n', '--name']:
                    action['name'] = value
                elif opt in ['-e', '--env', '--environment']:
                    action['env'] = value
                elif opt in ['-p', '--regex', '--pattern']:
                    action['pattern'] = value
                elif opt in ['-o', '--overwrite']:
                    action['overwrite'] = True
                elif opt in ['-r', '--repo', '--repository']:
                    action['repo'] = value
                elif opt in ['-i', '--id', '--project_id', '--project_stash_id']:
                    action['id'] = value
                elif opt in ['-u', '--intervalo']:
                    action['intervalo'] = value
                elif opt in ['-s', '--credential']:
                    action['credenciais'] = value
                else:
                    continue
    except (getopt.GetoptError, ValueError, KeyError, IndexError) as error:
        raise error

    # Validaçao de dados
    if not global_config.validate_runtime_options(conteudo=action):
        # print("Erro: Parametros invalidos ou falta parametros requisitos para acao desejada.")
        print("Argumentos: {0}".format(str(options)))
        Help()
        sys.exit(1)

    #
    if debug:
        print("Debug: enabled.")
        print("- Action: {0} {1} {2}\n\n".format(action['acao'], action['dado'], action['name']))

    # Cria instancias
    jnk = JenkinsCore()
    auto = Automation(jenkins=jnk, configuration=global_config, debug=debug)

    # Realiza procedimento de automacao
    if 'create' in action['acao']:
        if 'project' in action['dado']:
            auto.create_project_structure(project=action['name'])
            auto.create_project_roles(project=action['name'])
            auto.import_project_builds(project=action['name'], project_id=action['id'], dados=action)
        elif 'role' in action['dado']:
            auto.create_role(data=action)
        elif 'deploy_jobs' in action['dado']:
            auto.create_deploy_jobs(projeto=action['name'], repositorio=action['repo'])
        else:
            pass

    elif 'delete' in action['acao']:
        if 'project' in action['dado']:
            auto.delete_project_roles(project=action['name'])
            auto.delete_project_structure(project=action['name'])
        elif 'role' in action['dado']:
            auto.delete_role(data=action)
        elif 'deploy_jobs' in action['dado']:
            auto.delete_deploy_jobs(projeto=action['name'], repositorio=action['repo'])
        else:
            pass

    elif 'check' in action['acao']:
        if 'deploy_jobs' in action['dado']:
            status = auto.check_deploy_jobs(project=action['name'], repositorio=action['repo'])
            if type(status) is list and status != []:
                print("\nCriando jobs de deploy faltantes...")
                auto.create_missing_deploy_jobs(projeto=action['name'], ambiente= status, repositorio=action['repo'])
            else:
                print("\nINFO: Jobs de deploy já existem!")
                sys.exit(0)
        else:
            pass

    elif 'get' in action['acao']:
        pass

    else:
        pass
    #

    print('Processo finalizado.')
    sys.exit(0)


# =============================================================================================== #
#                                           Inicialização
# =============================================================================================== #
automate()
