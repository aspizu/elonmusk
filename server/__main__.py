import sqlite3
import time
from typing import Any

from flask import Flask, jsonify, request
from flask_cors import CORS
from sessions import Sessions

DB = "1.db"  # Path to database

app = Flask(__name__)
CORS(app)
sessions = Sessions()


def response_success(**kwargs: Any):
    return jsonify({"success": True, "exception": None, **kwargs})


def response_failure(exception: str, **kwargs: Any):
    return jsonify({"success": True, "exception": exception, **kwargs})


@app.get("/")
def hello_world():
    return "<h1>Hello, World!</h1>"


@app.get("/get_user/<int:user_id>")
def get_user(user_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", [user_id])
    a = cur.fetchone()
    if a is None or a[7] < 0:  # see /schema.sql:9
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


def hash_password(password: str) -> str:
    return password


@app.post("/register")
def register():
    if not request.json:
        raise Exception
    username: str = request.json["username"]
    email: str = request.json["email"]
    password: str = request.json["password"]
    bio: str = request.json["bio"]
    pfp: str = request.json["pfp"]
    if len(password) < 8:
        return response_failure("invalid_password")
    if not username.isalnum() and len(username) < 3:
        return response_failure("invalid_username")
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", [username])
    if cur.fetchone() is not None:
        return response_failure("user_exists")
    con.execute(
        "INSERT INTO users (username, email, password, bio, pfp, time, role) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [username, email, hash_password(password), bio, pfp, int(time.time()), 0],
    )
    con.commit()
    return response_success()


@app.post("/login")
def login():
    if not request.json:
        raise Exception
    username: str = request.json["username"]
    password: str = request.json["password"]
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT (id, password) FROM users WHERE username = ?", [username])
    _ = cur.fetchone()
    if _ is None:
        return response_failure("user_does_not_exist")
    user_id: int = _[0]
    hashed_password: str = _[1]
    if hash_password(password) != hashed_password:
        return response_failure("wrong_password")
    return response_success(token=sessions.new(user_id))


def main():
    app.run()


main()
