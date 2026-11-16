create database collage_journal
	character set utf8mb4
    collate utf8mb4_unicode_ci;

use collage_journal;

create table usuario (
    id_usuario int auto_increment primary key,
    nome varchar(50) not null,
    email varchar(100) unique not null,
    senha varchar(225) not null,
    foto mediumblob null,
    bio longtext null
);

create table relato_bug (
    id_relato int auto_increment primary key,
    relato longtext not null
);
