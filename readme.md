Jenkins automation module
---

Modulo python criado com o proposito de automatizar o processo de criação e remoção de projetos na ferramenta.


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


### Roadmap

- Integrar modulo a imagem
- Criar pipeline da automação (execução)


### Changelog

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