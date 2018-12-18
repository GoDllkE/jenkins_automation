Gerenciando projetos no jenkins
---

Este modulo permite também o gerenciamento dos jobs de deploy de um repositorio do seu projeto, tanto de forma apartada 
quanto integrada ao CI. Nesse arquivo, você verá como criar e/ou deletar os jobs de deploy de uma aplicação/repositorio. 

### Criando um job de deploy no jenkins
Para criar um novo conjunto de jobs de deploy no jenkins, execute com os seguintes parametros:

    $ jenkins_automation --create=job --name=seu_projeto --repo=https://lalalalala.git

Após inserir e prosseguir com o job, o mesmo vai garantir no seu projeto no jenkins, o job de deploy de cada ambiente
do seu repositorio/aplicação.   

### Deletando um projeto no jenkins
Para deletar um novo conjunto de jobs de deploy no jenkins, execute com os seguintes parametros:

    $ jenkins_automation --delete=job --name=seu_projeto --repo=https://lalalalala.git

Após inserir e prosseguir com o job, o mesmo vai garantir que os jobs de deploy dessa aplicacao/repositorio sejam removidos.
Obs: Os jobs de deploy que estiverem em execução serão interrompidos.
