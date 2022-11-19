import sqlite3

from flask import Flask

con = sqlite3.connect("1.db")
app = Flask(__name__)


@app.get("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


def main():
    app.run()
    con.commit()


main()
