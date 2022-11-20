import os
import sqlite3
import sys

try:
    os.remove(sys.argv[1])
except FileNotFoundError:
    pass
con = sqlite3.connect(sys.argv[1])
with open("schema.sql", "r") as fp:
    con.executescript(fp.read())
