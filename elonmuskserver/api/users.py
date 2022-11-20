import sqlite3
import time

from flask import request

from ..__init__ import DB, app, sessions
from ..sessions import hash_password
from .lib import response_failure, response_success


@app.get("/get_used_id/<username>")
def get_user_id(username: str):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT id FROM users WHERE username = ?", [username])
    _ = cur.fetchone()
    if _ is None or _[1] < 0:  # see /schema.sql:9
        return response_failure("user_does_not_exist")
    return response_success(user_id=_[0])


@app.get("/get_user/<int:user_id>")
def get_user(user_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", [user_id])
    _ = cur.fetchone()
    if _ is None or _[7] < 0:  # see /schema.sql:9
        return response_failure("user_does_not_exist")
    return response_success(
        username=_[1],
        email=_[2],
        # password=a[3], bruh dont return password
        bio=_[3],
        pfp=_[4],
        time=_[5],
    )


@app.get("/get_user_follower_count/<int:user_id>")
def get_user_follower_count(user_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT COUNT(*) FROM followers WHERE user_id = ?", [user_id])
    _ = cur.fetchone()
    return response_success(count=_[0])


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


@app.post("/update_profile")
def update_profile():
    if not request.json:
        raise Exception
    token: int = request.json["token"]
    user_id: int = sessions.get(token)
    diff = request.json["diff"]
    if (
        not all(i in ["email", "bio", "pfp"] for i in diff.keys())
        or len(diff.keys) == 0
    ):
        return response_failure("invalid_fields")
    con = sqlite3.connect(DB)
    sets = " ".join(f"{i} = ?" for i in diff.keys())
    con.execute(f"UPDATE users SET {sets} WHERE id = ?", [*diff.values(), user_id])
    con.commit()
    return response_success()


@app.post("/follow_user")
def follow_user():
    if not request.json:
        raise Exception
    token: int = request.json["token"]
    follower_id: int = sessions.get(token)
    user_id: int = request.json["user_id"]
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO followers (follower_id, user_id) VALUES (?, ?)",
        [follower_id, user_id],
    )
    con.commit()
    return response_success()


@app.post("/unfollow_user")
def unfollow_user():
    if not request.json:
        raise Exception
    token: int = request.json["token"]
    follower_id: int = sessions.get(token)
    user_id: int = request.json["user_id"]
    con = sqlite3.connect(DB)
    con.execute(
        "DELETE FROM followers WHERE follower_id = ? AND user_id = ?",
        [follower_id, user_id],
    )
    con.commit()
    return response_success()
