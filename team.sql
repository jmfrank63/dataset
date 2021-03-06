SET sql_mode = 'ANSI';
SET GLOBAL sql_mode = 'ANSI';
DROP DATABASE if exists dkm_team;
CREATE DATABASE dkm_team;
use dkm_team;

DROP TABLE IF EXISTS TEAM;
CREATE TABLE TEAM
(
    T_ID   INT PRIMARY KEY ,
    T_COUNTRY  VARCHAR(32)
);

DROP TABLE IF EXISTS COMPETITOR;
CREATE TABLE COMPETITOR
(
    C_ID   INT PRIMARY KEY,
    C_NAME  VARCHAR(32),
    T_ID INT REFERENCES TEAM (T_ID)
);

DROP TABLE IF EXISTS EVENT;
CREATE TABLE EVENT
(
       E_ID INT PRIMARY KEY,
       E_NAME VARCHAR(32),
       E_CATEGORY  VARCHAR(10)
);

DROP TABLE IF EXISTS RESULT;
CREATE TABLE RESULT (
    E_ID INT PRIMARY KEY ,
    C_ID INT REFERENCES COMPETITOR (C_ID),
    PLACE VARCHAR(32)
);

INSERT INTO TEAM (T_ID, T_COUNTRY) VALUES (27, 'great britain');

INSERT INTO COMPETITOR (C_ID, C_NAME, T_ID) VALUES (350, 'Luke Skywalker', 27);

INSERT INTO EVENT (E_ID, E_NAME, E_CATEGORY) VALUES (89, 'men 100m', 'athletics');

INSERT INTO RESULT (E_ID, C_ID, PLACE) VALUES (89, 350, 2);
