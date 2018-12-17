Gerenciando projetos no jenkins
---
> De: 17/12/2018

> Versão atual: 5.1.2

> Por: Gustavo Toledo

Este modulo permite o fácil gerenciamento entre projetos que vão entrar ou sair do jenkins de forma centralizada e a 
facilitar o controle e gestão do que ocorre no nosso jenkins.
Nesse arquivo, você verá como criar, deletar e atualizar um projeto no jenkins. 

### Criando um projeto no jenkins
Para criar um novo projeto no jenkins, execute este job: [project_automation](https://jenkins-central.pontoslivelo.com.br/blue/organizations/jenkins/automations%2Fproject_automation/activity), e faça o seguinte:
1) Selecione a opção para criar um projeto
2) Insira o ID do projeto no stash
3) Clique no botão 'prosseguir'

Após inserir e prosseguir com o job, o mesmo vai garantir que seu projeto no jenkins, assim como todos os seus 
repositorios atuais e futuros e também (em implementação) vai garantir o deploy da sua aplicação!
Seu projeto no jenkins vai seguir a seguinte estrutura:

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

Na pasta **build**, você vai encontrar todos os seus repositorios do Stash/Bitbucket e é onde ocorre
todos os builds.
Na pasta **deploy**, você vai encontrar todos os jobs de deploy de cara um dos seus repositorios (em implementação)
Na pasta **QA/testes**, você vai encontrar todos os jobs referente a testes.   

### Deletando um projeto no jenkins
Para deletar um projeto no jenkins, execute este job: [project_automation](https://jenkins-central.pontoslivelo.com.br/blue/organizations/jenkins/automations%2Fproject_automation/activity), e faça o seguinte:
1) Selecione a opção para deletar um projeto
2) Insira o ID do projeto no stash
3) Clique no botão 'prosseguir'

Após inserir e prosseguir com o job, o mesmo vai garantir que todas as coisas referentes a esse projeto
no jenkins sejam *exterminados* (isso inclui jobs em execução)
  

### Atualizando um projeto no jenkins  
Infelizmente, por limitações da API, não há uma maneira de atualizar o projeto. 

**Caso precise apenas repor um job ou uma pasta, você pode rodar novamente o o job: [project_automation](https://jenkins-central.pontoslivelo.com.br/blue/organizations/jenkins/automations%2Fproject_automation/activity) de forma a criar o 
projeto novamente e e ele vai criar apenas o que não existir.**  

**Caso precise restaurar uma configuração que veio da automaçao, será necessário deletar e depois criar novamente o projeto 
no jenkins da forma que foi explicado anteriormente, onde você perderá todo o histórico de execuções dos jobs no jenkins.**  

Conforme a API for atualizando e novas funcionalidades implementadas, uma maneira melhor de autalizar projetos será 
planejado e implementado nesse programa. 

