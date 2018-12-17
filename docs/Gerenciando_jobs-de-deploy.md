Gerenciando projetos no jenkins
---
De: 17/12/2018
Versão atual: 5.1.0
Por: Gustavo Toledo
---

Este modulo permite também o gerenciamento dos jobs de deploy de um repositorio do seu projeto, tanto de forma apartada 
quanto integrada ao CI. Nesse arquivo, você verá como criar e/ou deletar os jobs de deploy de uma aplicação/repositorio. 

### Criando um job de deploy no jenkins
Para criar um novo conjunto de jobs de deploy no jenkins, execute este job: [project__job_automation](https://jenkins-central.pontoslivelo.com.br/blue/organizations/jenkins/automations%2Fproject_deploy-job_automation/activity), e faça o seguinte:
1) Selecione a opção para criar
2) Insira o ID do projeto no stash
3) Insira a URL do repositorio (ex: https://stash.pontoslivelo.com.br/scm/XX/YYY.git)
4) Clique no botão 'prosseguir'

Após inserir e prosseguir com o job, o mesmo vai garantir no seu projeto no jenkins, o job de deploy de cada ambiente
do seu repositorio/aplicação.   

### Deletando um projeto no jenkins
Para deletar um novo conjunto de jobs de deploy no jenkins, execute este job: [project__job_automation](https://jenkins-central.pontoslivelo.com.br/blue/organizations/jenkins/automations%2Fproject_deploy-job_automation/activity), e faça o seguinte:
1) Selecione a opção para deletar
2) Insira o ID do projeto no stash
3) Insira a URL do repositorio (ex: https://stash.pontoslivelo.com.br/scm/XX/YYY.git)
4) Clique no botão 'prosseguir'

Após inserir e prosseguir com o job, o mesmo vai garantir que os jobs de deploy dessa aplicacao/repositorio sejam removidos.
Obs: Os jobs de deploy que estiverem em execução serão interrompidos.
