CREATE SCHEMA IF NOT EXISTS etl4all;
USE etl4all;
CREATE TABLE IF NOT EXISTS address (
    id INT AUTO_INCREMENT,
    latitude VARCHAR(255),
    longitude VARCHAR(255),
    rua VARCHAR(255),
    numero VARCHAR(255),
    bairro VARCHAR(255),
    cidade VARCHAR(255),
    cep VARCHAR(255),
    estado VARCHAR(255),
    pais VARCHAR(255),
    PRIMARY KEY (id)
)  ENGINE=INNODB;