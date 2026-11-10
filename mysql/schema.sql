create database collage_journal;

use collage_journal;

create table usuario (
    id_usario int auto_increment primary key,
    nome varchar(50) not null,
    email varchar(100) not null,
    senha varchar(225) not null,
    bio longtext null
);

create table relato_bug (
    id_relato int auto_increment primary key,
    relato longtext not null
);

