create database ebweb default character set utf8mb4;

use ebweb;

select * from users;

show create table users;

alter table users modify gender varchar(1); # Remove the NOT NULL constraint