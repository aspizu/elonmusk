import sqlite3
import time

from flask import request

from ..__init__ import DB, app, sessions
from .lib import response_failure, response_success


@app.get("/get_post/<int:post_id>")
def get_post(post_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "SELECT (user_id, body, time, visible) FROM posts WHERE id = ?", [post_id]
    )
    _ = cur.fetchone()
    if _ is None or not _[3]:
        return response_failure("post_does_not_exist")
    return response_success(user_id=_[0], body=_[1], time=_[2])


@app.post("/create_post")
def create_post():
    if not request.json:
        raise Exception
    user_id = sessions.get(request.json["token"])
    body: str = request.json["body"]
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO posts (user_id, body, time, visible) VALUES (?, ?, ?, ?)",
        [user_id, body, int(time.time()), True],
    )
    con.commit()
    return response_success()


@app.post("/like_post")
def like_post():
    if not request.json:
        raise Exception
    user_id = sessions.get(request.json["token"])
    post_id: int = request.json["post_id"]
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO post_likes (user_id, post_id, is_like) VALUES (?, ?, ?)",
        [user_id, post_id, True],
    )
    con.commit()
    return response_success()


@app.post("/dislike_post")
def dislike_post():
    if not request.json:
        raise Exception
    user_id = sessions.get(request.json["token"])
    post_id: int = request.json["post_id"]
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO post_likes (user_id, post_id, is_like) VALUES (?, ?, ?)",
        [user_id, post_id, False],
    )
    con.commit()
    return response_success()


@app.post("/unlike_post")
def unlike_post():
    if not request.json:
        raise Exception
    user_id = sessions.get(request.json["token"])
    post_id: int = request.json["post_id"]
    con = sqlite3.connect(DB)
    con.execute(
        "DELETE FROM post_likes WHERE user_id = ? AND post_id = ?", [user_id, post_id]
    )
    con.commit()
    return response_success()


@app.get("/get_post_like_count/<int:post_id>")
def get_post_like_count(post_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM post_likes WHERE post_id = ? AND is_like = true",
        [post_id],
    )
    _ = cur.fetchone()
    return response_success(count=_[0])


@app.get("/get_post_dislike_count/<int:post_id>")
def get_post_dislike_count(post_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM post_likes WHERE post_id = ? AND is_like = false",
        [post_id],
    )
    _ = cur.fetchone()
    return response_success(count=_[0])
