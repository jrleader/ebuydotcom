drop database ebmall;

create database ebmall default character set utf8mb4;

SHOW VARIABLES LIKE 'max_allowed_packet';

use ebmall;

show tables;

describe shops;

describe products;

describe favorite_products;

select * from shops;