CREATE SCHEMA IF NOT EXISTS etl4all;
USE etl4all;
CREATE TABLE IF NOT EXISTS address (
    id INT AUTO_INCREMENT,
    latitude VARCHAR(255),
    longitude VARCHAR(255),
    street_number VARCHAR(255),
    street_name VARCHAR(255),
    district_name VARCHAR(255),
    city_name VARCHAR(255),
    state_name VARCHAR(255),
    country_name VARCHAR(255),
    postal_code VARCHAR(255),
    PRIMARY KEY (id)
)  ENGINE=INNODB;


