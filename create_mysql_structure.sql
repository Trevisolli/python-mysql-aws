create database python_course;
use python_course;

select version(), database();

drop table employees;

create table employees (id bigint primary key, first_name varchar(100), last_name varchar(100), birth_date date, exported varchar(1) default 'N');

insert into employees (id, first_name, last_name, birth_date)
values (1, 'John', 'Tyler', '2000-12-15');

insert into employees (id, first_name, last_name, birth_date)
values (2, 'Scott', 'Burleson', '1970-04-03');

insert into employees (id, first_name, last_name, birth_date)
values (3, 'Mary', 'Smith', '1998-07-28');

insert into employees (id, first_name, last_name, birth_date)
values (4, 'Bruce', 'Lee', '1940-11-27');

insert into employees (id, first_name, last_name, birth_date)
values (5, 'Steven', 'Tyler', '1948-03-26');

insert into employees (id, first_name, last_name, birth_date)
values (6, 'Michael', 'Jackson', '1958-08-29');

-- Após rodar o arquivo no Python, caso deseje criar novamente, atualizar os registros pra "N"
-- e rodar conectar_mysql.py.
select * from employees;

update employees set exported = 'N' where id > 0;


