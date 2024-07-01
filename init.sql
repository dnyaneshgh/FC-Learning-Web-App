
CREATE DATABASE IF NOT EXISTS FlashCard;
USE FlashCard;

CREATE TABLE IF NOT EXISTS Questions (
    ID int NOT NULL auto_increment,
    Topic varchar(255) NOT NULL,
    Question varchar(255),
    Answer varchar(255),
    Hint varchar(255),
    primary key(ID)
);
