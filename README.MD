<p align="center">
  <a href="https://www.linkedin.com/in/Trevisolli">
    <img width="140" src="https://github.com/Trevisolli/python-mysql-aws/blob/master/images/python_mysql.png"/>  
  </a>  
  <h2 align="center">Conexão no MySQL via Python e gravação de Arquivos</h2>
  
   
  <p align="center">
  <a href="https://www.linkedin.com/in/Trevisolli">
    <img alt="Autor: Paulo Trevisolli" src="https://img.shields.io/badge/Autor-Paulo%20Trevisolli-green">
  </a>
  <img alt="Licença do Projeto" src="https://img.shields.io/badge/LICENSE-MIT-green"/>
<p>
  <p align="center">Repositório criado para manter os artefatos de resolução, ganho de conhecimento, de exercício de Python conectando em base de dados MySQL, extraíndo seus registros e gravando-os em um arquivo TXT.</p> 
  <p align="center"><b>(16/Dezembro/2022)</b></p>  
</p>


# Introdução 
Irei disponibilizar aqui os arquivos para reprodução e explicação dos principais assuntos para que o projeto funcione com sucesso.

Sugestões de melhoria, são sempre bem vindas!

## biblioteca

Deve ser instalado o conector do Python, para o BD MySQL, conforme abaixo:
```
pip install mysql-connector-python
```

## <a href="https://github.com/Trevisolli/python-mysql-aws/blob/master/db.properties">db.properties</a>

Arquivo que especifica as características/propriedades para conexão em um BD MySQL. 
A versão da base de dados utilizada neste projeto, foi a 8.0.23, disponível para download <a href="https://downloads.mysql.com/archives/get/p/25/file/mysql-installer-community-8.0.30.0.msi">aqui</a>.

Abaixo, segue a visualização do arquivo <b>db.properties</b> onde, o lado esquerdo, em azul, são as propriedades de configuração, que devem ser mantidas com este nome, e, ao lado direto,de cor branca, os valores, que devem ser alterados de acordo com a sua instalação do MySQL.
<p align="center">
  <img width="250" src="https://github.com/Trevisolli/python-mysql-aws/blob/master/images/db_properties.PNG"/>  
</p>

Lembrando que, este arquivo (<b>db.properties</b>) é essencial para que este projeto funcione corretamente, portanto, deve ser configurado exatamente de acordo com as configurações de instalação do BD e, deve estar no diretório do projeto, onde se encontra o arquivo <b>conectar_mysql.py</b>.

## <a href="https://github.com/Trevisolli/python-mysql-aws/blob/master/create_mysql_structure.sql">create_mysql_structure.sql</a>

Arquivo que especifica as estruturas de dados que devem ser criadas no BD MySQL. 

Abaixo, segue a visualização do arquivo <b>create_mysql_structure.sql</b>:
<p align="center">
  <img width="450" src="https://github.com/Trevisolli/python-mysql-aws/blob/master/images/create_mysql_structure.PNG"/>  
</p>

Deve ser aplicado este script no seu banco de dados, para criação da tabela <b>employees</b>, que conterá os nossos cadastros.

Este script também contém os comandos de carga de dados (inserts) que foram realizados que, por motivos didáticos foram realizados diretamente no BD e não via Python.

## <a href="https://github.com/Trevisolli/python-mysql-aws/blob/master/conectar_mysql.py">conectar_mysql.py</a>

Este é o principal arquivo do projeto, que contém os métodos e, a chamada principal.
Resumidamente, ele executa as seguintes operações:
<ol>
  <li>Verifica se existem registros na base de dados MySQL, tabela employees, onde o campo "exported" seja "N"</li>
  <li>Caso existam registros nessas condições: </li>
  <ol>
    <li>Retorna uma Lista, contendo o id, first_name e last_name do empregado</li>  
    <li>Grava esse registro da base de dados em um arquivo chamado employees_list.txt (no modo append, adicionando no final)</li>      
    <li>Seta o campo "exported" para "S", para que numa próxima execução, esse registro não seja enviado</li>          
    <li>Após percorrida a lista, grava o arquivo employees_list.txt no mesmo diretório da execução do comando conectar_mysql.py</li>              
    <li>Exibe mensagem de arquivo criado/atualizado com sucesso.</li>              
  </ol>
  <li>Caso não existam registros nessas condições (exported="N"), apenas exibe uma mensagem ao usuário. </li>
</ol>

Imagem da execução do projeto:

<p align="center">
  <img width="450" src="https://github.com/Trevisolli/python-mysql-aws/blob/master/images/execution_results.PNG"/>  
</p>

Produto final, sendo o arquivo criado:

<p align="center">
  <img width="250" src="https://github.com/Trevisolli/python-mysql-aws/blob/master/images/employees_list.PNG"/>  
</p>

<b>Nota Importante:</b> Sempre que se adicionar um novo registro no Banco de Dados MySQL, o arquivo conectar_mysql.py pode ser executado novamente, pois o mesmo verifica as diferenças no BD que ainda não foram para o arquivo texto, e o atualiza.

<b>Nota Importante2:</b> A segunda fase deste projeto consiste, em recuperar este arquivo gerado no sistema Operacional e, enviá-lo à um Bucket S3 na AWS (Em breve!).
