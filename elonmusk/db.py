import sqlite3


def connect():
    return sqlite3.connect("1.db")


def cursor():
    con = connect()
    return con, con.cursor()
