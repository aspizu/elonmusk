import sqlite3

from flask import Flask, jsonify, request
from flask_cors import CORS

DB = "1.db"
app = Flask(__name__)
CORS(app)


@app.get("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.get("/get_user/<int:user_id>")
def get_user(user_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", [user_id])
    a = cur.fetchone()
    if a is None or a[7] < 0:
        return jsonify({"error": "notfound"})
    return jsonify(
        {
            "username": a[1],
            "bio": a[4],
            "pfp": a[5],
            "time": a[6],
        }
    )


@app.get("/get_post/<int:post_id>")
def get_post(post_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM posts WHERE id = ?", [post_id])
    a = cur.fetchone()
    if a is None or not a[4]:
        return jsonify({"error": "notfound"})
    return jsonify(
        {
            "user_id": a[1],
            "body": a[2],
            "time": a[3],
        }
    )


@app.get("/get_comment/<int:comment_id>")
def get_comment(comment_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM comments WHERE id = ?", [comment_id])
    a = cur.fetchone()
    if a is None or not a[5]:
        return jsonify({"error": "notfound"})
    return jsonify(
        {
            "user_id": a[1],
            "post_id": a[2],
            "body": a[3],
            "time": a[4],
        }
    )


@app.post("/register")
def register():
    # if user exists
    #    error
    # create user
    # return success
    ...


def main():
    app.run()


main()
