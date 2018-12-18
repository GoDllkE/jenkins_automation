Gerenciando roles no jenkins
---
De: 
Versão atual: 
Por: 
---

#### Criando uma role no jenkins
Para criar um nova role no jenkins, execute o binario com estes parametros:

    $ jenkins_automation --create=role --type=role_type --name=role_name --pattern=sua_regex --overwrite

Executando a linha, uma nova role será criada no jenkins.

**type:** É o tipo de role a ser criada (globalRole ou projectRole).

**name:** É o nome da role que será criada.

**pattern:** É a regex (em caso de *projectRole*) na qual se aplica sua role.

**overwrite:** Opcional para atualizar a role caso ela ja exista (compara via campo name).
   

#### Deletando um projeto no jenkins
Para deletar um projeto no jenkins, execute o binario com estes parametros:

    $ jenkins_automation --delete=project --name=seu_projeto

Após inserir e prosseguir com o job, o mesmo vai garantir que todas as coisas referentes a esse projeto
no jenkins sejam *exterminados* (isso inclui jobs em execução)
  

#### Deletando uma role no jenkins  
Para deletar uma ou mais roles no jenkins, execute o binario com estes parametros:

    $ jenkins_automation --delete=role --type=role_type --name=role1

ou

    $ jenkins_automation --delete=role --type=role_type --name=role1,role2,role3,roleN

Executando a linha, uma ou mais roles serão deletadas do jenkins.

**type:** É o tipo de role a ser criada (globalRole ou projectRole).

**name:** É o nome da role que será deletada. Pode ser um unico nome (ex: role1) ou uma lista de roles separadas por virgula (ex: role1,role2,role3,role4,roleN)
