import shlex
from itertools import groupby

import mariadb
import sys

BEGIN_STMT = """
SET sql_mode = 'ANSI';
SET GLOBAL sql_mode = 'ANSI';
DROP DATABASE if exists {};
CREATE DATABASE {};
use {};"""


def db_connect():
    # Connect to MariaDB Platform
    try:
        conn = mariadb.connect(user="root", password="dkm", host="127.0.0.1", port=3306)
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    return conn


def db_create(conn, year, data):
    cur = conn.cursor()
    try:
        statement = "SET sql_mode = 'ANSI'"
        print(statement + ";")
        cur.execute(statement)
        statement = "SET GLOBAL sql_mode = 'ANSI'"
        print(statement + ";")
        cur.execute(statement)
        statement = f"drop database if exists dkm_exam_{year}"
        print(statement + ";")
        cur.execute(statement)
        statement = f"create database dkm_exam_{year}"
        print(statement + ";")
        cur.execute(statement)
        statement = f"use dkm_exam_{year}"
        print(statement + ";")
        cur.execute(statement)
    except mariadb.Error as e:
        print(f"Error: {e}")
    # print(year)
    for table in data:
        lines = table.split(":")
        header = lines[0]
        header = header.replace("(", "").replace(")", "").replace(",", "").split(" ")
        table_name = header[0]
        columns = header[1:]

        statement = f'DROP TABLE IF EXISTS "{table_name }"'
        print(statement + ";")
        cur.execute(statement)
        statement = f'CREATE TABLE "{table_name}" '
        statement += "({})".format(
            ", ".join(map(lambda x: x + " VARCHAR(32)", columns))
        )
        print(statement + ";")
        cur.execute(statement)
        for values in lines[1:]:
            values = shlex.split(values.replace("(", "").replace(")", "").replace(",", ""))
            # values = fake_values(columns, values)
            statement = 'INSERT INTO "{}" ({}) VALUES ({})'.format(
                table_name,
                ", ".join(columns),
                ", ".join(map(lambda x: "'" + str(x.replace(",", "")) + "'", values)),
            )
            print(statement + ";")
            cur.execute(statement)


def fake_values(columns, values):
    for column in zip(columns, values):
        answer = list(map(str.strip, input(f"Enter type, low, high for {column}:").split(",")))
        print(answer)
    return values


def main(filename):
    with open(filename, "r") as data_file:
        data = data_file.read().splitlines()
    res = [list(sub) for ele, sub in groupby(data, key=bool) if ele]

    conn = db_connect()
    years = {}
    for year in res:
        years[year[0]] = year[1:]
    for year in years:
        db_create(conn, year, years[year])
    conn.close()


if __name__ == "__main__":
    main("data.txt")
