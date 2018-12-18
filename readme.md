# Jenkins Automation
---

Modulo python criado com o proposito de automatizar o processo de criação e remoção de projetos na ferramenta.

#### Requisitos

Requisitos de execução do modulo:
- Python 3.6 (preferencia para versão latest)
- PyYaml
- Requests

Requisitos de construção do modulo:
- Setuptools 
- PyInstaller
- PyYaml
- Requests

#### Instalando dependencias 

Execute o comando:

    $ pip install -r requirements.txt

#### Compilando esse modulo para um unico arquivo

Primeiro, execute:
    
    $ python setup.py develop && python setup.py sdist
    

A seguir, execute:

    $ pyinstaller --onefile --path automation/ --console bin/automation

**Obs:** *O "binário" será gerado de acordo com a sua distribuição linux e as versões do GCC e LIBC.* 

#### Gerando a imagem docker com este binário

Na raiz do projeto, Execute:

    $ docker build . -t GoDlikE/jenkins_automation:latest -f docker/Dockerfile

Assim, vai gerar uma imagem com o binario. Para testar a imagem, execute:

    $ docker run -it --rm --name jenkins_automation GoDlikE/jenkins_automation:latest '-h' 

Após executar o comando anterior, o help-me deve aparecer conforme o que foi escrito na [classe de auxilio](automation/Help.py).


#### Sobre os arquivos de configurações

O modulo carrega as configurações a partir de um arquivo YAML de três pontos diferentes e prioritários, sendo eles (em ordem de prioridade):
1) Da variavel de ambiente: *JENKINS_AUTOMATION_CONFIG*
2) Do caminho no host: */etc/jenkins_automations/config.yaml*
3) *Carregamento interno do modulo*

Os dois primeiros podem ser alterados facilmente, atualizando os valores da [classe de configuração](automation/Configurator.py) para as nomeclaturas ou caminhos desejados, assim como os parametros e outros.

Ou seja, no momento de executar, este programa olha primeiro se existe uma VARIAVEL DE AMBIENTE LINUX respectiva a
configuração que ele precisa, que se existir, deve ter o valor para um caminho onde possui um YAML com as chaves que
pode ser consultado [aqui](automation/resources/config.yaml).

Caso não encontre essa variavel ou arquivo, ele vai buscar
essas configurações em */etc/jenkins_automations/config.yaml*

Caso também não encontre nesse local, ele tentará fazer o
carregamento interno, que devido as possíveis alterações de ambiente pode ocorrer erros.

#### O que contem nas configurações?

Basicamente, tudo!
No arquivo de configuração é guardado toda configuração de como deve ser criado as roles e a estrutura de pastas a criar no jenkins. Atualmente, ele está criando neste modelo:

``` 
projects
└── seu_projeto
    ├── build
    │   ├── repo1
    │   ├── repo2
    │   └── repoN
    ├── deploy
    │   ├── dev
    │   ├── prd
    │   ├── sit
    │   └── uat
    └── qa
``` 

Mas voce pode adaptar a sua necessidade a partir deste arquivo [config.yaml](automation/resources/config.yaml), na chave **folder_structure**

Nele, também está a configuração das roles e as permissões que cada role terá.

**Então, caso precise alterar o padrão. Altere nesse arquivo**.

#### Configurações da automação

Este programa utiliza um arquivo externo de configurações para facilitar a manutenção e troca de padrões.
O mesmo pode ser consultado [aqui](automation/resources/config.yaml)

Além do arquivo externo de configurações gerais, existe o arquivo de configuração dos jobs de deploy,
que pode ser consultado [aqui](automation/resources/job_config.xml)

#### Observações
*Existe a versão proprietária deste modulo que complementa a integração jenkins <-> stash/bitbucket e também elimina aproximadamente 90% dos processos manuais que nesta versão Open Source possui, além de possuir monitoria e integração com Jira.*