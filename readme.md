Jenkins automation module
---

Modulo python criado com o proposito de automatizar o processo de criação e remoção de projetos na ferramenta.

### Uso
Para utilizar este modulo, tenha docker-ce em sua máquina e execute o seguinte comando:

    $ docker pull registry.ng.bluemix.net/livelo/jenkins_automation:latest
    
Em seguida, acesse-a:
    
    $ docker run -it --rm --name jenkins_automation  registry.ng.bluemix.net/livelo/jenkins_automation

Agora, dentro da imagem do modulo, execute:

    $ /bin/jenkins_automation -h
    
A partir da ajuda exibida em tela, realize as operações desejadas.   

### Configurações

O modulo carrega as configurações a partir de um arquivo YAML de três pontos diferentes e prioritários,
sendo eles (em ordem de prioridade):
1) Da variavel de ambiente: *JENKINS_AUTOMATION_CONFIG*
2) Do caminho no host: */etc/jenkins_automations/config.yaml*
3) *Carregamento interno do modulo*

### O que contem nas configurações?

Basicamente, tudo!
No arquivo de configuração é guardado toda configuração baseada na arquitetura estrutural definida
no jenkins, que pode ser encontranda no confluence.
Nele, existe a configuração da criação de estrutura de pastas por projeto e também o padrão das roles 
de projeto, isto é, role de *view*, *build*, *deploy* e etc. 
**Então, caso precise alterar o padrão. Altere nesse arquivo**.

### Template do arquivo de configuração

Na verdade não é um template, mas voce pode usar o arquivo de configuração interna do modulo como um template 
para sua necessidade, que se encontra [aqui](automation/resources/config.yaml) 

### Requisitos

Requisitos de execução do modulo:
- Python 3.7.1
- PyYaml
- Requests

Requisitos de construção do modulo:
- Setuptools 
- PyInstaller
- PyYaml
- Requests


### Changelog

**Versão: 5.0.0**
- Removido parametro essencial de execução (name)
- Adicionado e implementado nova classe de requisições do Bitbucket
- Atualizado funções da automação para compatibilidade da nova implementação.

**Versão: 4.2.13**
- Corrigido template do job de deploy [job](automation/resources/job_config.xml). Agora adicionado ao interpretador do jenkins os parametros além da declaração via pipeline.

**Versão: 4.2.12**
- Corrigido nomeclatura na criação das roles estarem vazias.
- Corrigido regex das roles de projetos estarem com ID do projeto ao invés do nome da pasta.
- Atualizado [help-me](automation/Help.py) com exemplos respectivos a versão do modulo.
- Alterado nomeclatura das roles de um projeto para utilizar ID do projeto do bitbucket.
- Removido linhas desnecessárias de arquivos de configuração e outros.
- Outros bugs menores corrigidos.

**Versão: 4.2.8**
- Corrigido XML's responsáveis pelos jobs de deploy e importação de projeto stash.
- Alterado nomeclatura das roles de um projeto para utilizar ID do projeto do bitbucket.

**Versão: 4.2.0**
- Adicionado feature de verificação/garantia dos jobs de deploy de um repositorio.

**Versão: 4.1.0**
- Adicionado feature de importação de projeto do stash para o jenkins.
- Atualizando arquivos de configuração.

**Versão: 4.0.2**
- Modulo completamente refatorado
- Alterado fluxo de chamadas e dados utilizados.
- Corrigido função de interfacionamento da automação.
- Corrigido nomeclatura de funções para entrada de nova feature.

**Versão: 3.10.8**
- Removido mensagens desnecessárias.
- Alterado entrypoint da imagem por compatibilidade do pipeline.
- Removido testes com imagem docker. (problema identificado como DNS - infra)
- Corrigido problema de build da imagem docker.

**Versão: 3.10.0**
- Adicionado testes para imagem docker, após sua construção.

**Versão: 3.9.0**
- Adicionado imagem docker para construção de outras imagens docker ao pod
do kubernetes.
- Corrigido sessões do pipeline invertidas.

**Versão: 3.8.0**
- Adicionado requisitos para construção de imagem docker
- Corrigido bug referente a executar a aplicação sem argumentos.

**Versão: 3.7.1**
- Adicionado feature de criação da estrutura de pastas do projeto 
- Adicionado feature de remoção da estrutura de pastas do projeto
- Alterado estrutura do arquivo de configuração, por compatibilidade.
- Adicionado estruturas ao fluxo principal
- Adicionado testes na construção do modulo (teste simples e composto)


**Versão: 3.5.1**
- Criação de roles simples e compostas funcionando corretamente.
- Definido arquivo de configuração de toda a automação.
- Flexibilidade do modulo carregar outros arquivos de configuração
- Flexibilidade na atualização das atuais automações.
- Adicionado testes de execuçao diversos ao pipeline, simulando cenários reais.

**Versão: 3.1.1**
- Substituido classe de configurações internas por arquivo de properties (YAML)
 
[ Changelogs perdidos ]

**Versão: 2.0.2**
- Adicionado estagio de criação de TAG's