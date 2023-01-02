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

Para se instalar as demais bibliotecas, como <b>python-dotenv</b>, <b>boto3</b>  etc:
```
pip install python-dotenv
pip install awscli
pip install boto3
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

Neste caso, seguindo a instalação sugerida no <a href="https://downloads.mysql.com/archives/get/p/25/file/mysql-installer-community-8.0.30.0.msi">Link acima</a>, foi marcada a opção de MySQL Workbench, que utilizei como IDE para questões de tarefas de banco de dados.  

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

## <a href="https://github.com/Trevisolli/python-mysql-aws/blob/master/pys3.py">pys3.py</a>

Este arquivo funciona como um módulo, que provê funções de manipulação de Buckets e Arquivos no Amazon S3 e o mesmo é importado no arquivo <a href="https://github.com/Trevisolli/python-mysql-aws/blob/master/conectar_mysql.py">conectar_mysql.py</a>.

Após a geração do arquivo employees_list.txt, o mesmo é copiado para um bucket S3 da Amazon.

Resumidamente, ele executa as seguintes operações na AWS (S3):
<ol>
  <li>Leitura de variáveis de ambiente<b>*</b>, para proteção de dados sensíveis da AWS</li>
  <li>Criação de Bucket</li>
  <li>Upload de Arquivos</li>
  <li>Download de Arquivos</li>
  <li>Deleção de Arquivos</li>  
  <li>Cópia de Arquivos entre Buckets</li>  
  <li>Listagem de Arquivos do Bucket</li>   
</ol>

<b>* Nota importante sobre Variáveis de Ambiente: </b> Neste projeto foi utilizada a biblioteca <b><a href="https://pypi.org/project/python-dotenv/">python-dotenv</a></b> para se trabalhar com arquivos de configuração de variáveis de ambiente, sem que os valores sensíveis fiquem expostos no seu código. Um exemplo bem prático de como importar e utilizar esta biblioteca, está no vídeo à seguir, do <a href="https://www.youtube.com/watch?v=Jp5inslWuKg">Téo Me Why</a>.
  
Imagens da execução do projeto, com todo o fluxo:  

Conectar no mysql e gerar arquivo local:

<p align="center">
  <img width="250" src="https://github.com/Trevisolli/python-mysql-aws/blob/master/images/execution_results_2.PNG"/>  
</p>

Copiar arquivo para a AWS S3.

<p align="center">
  <img width="250" src="https://github.com/Trevisolli/python-mysql-aws/blob/master/images/bucket_001.PNG"/>  
</p>

<p align="center">
  <img width="250" src="https://github.com/Trevisolli/python-mysql-aws/blob/master/images/employees_list_inside_bucket.PNG"/>  
</p>



