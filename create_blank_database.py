import os
import sqlite3
import sys

os.remove(sys.argv[1])
con = sqlite3.connect(sys.argv[1])
with open("schema.sql", "r") as fp:
    con.executescript(fp.read())
