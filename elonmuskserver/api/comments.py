import sqlite3
import time

from flask import request

from ..__init__ import DB, app, sessions
from .lib import response_failure, response_success


@app.get("/get_comment/<int:comment_id>")
def get_comment(comment_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "SELECT (user_id, post_id, body, time, visible) FROM comments WHERE id = ?",
        [comment_id],
    )
    _ = cur.fetchone()
    if _ is None or not _[4]:
        return response_failure("post_does_not_exist")
    return response_success(user_id=_[0], post_id=_[1], body=_[2], time=_[3])


@app.post("/create_comment")
def create_comment():
    if not request.json:
        raise Exception
    user_id = sessions.get(request.json["token"])
    post_id: int = request.json["post_id"]
    body: str = request.json["body"]
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO comments (user_id, post_id, body, time, visible) "
        "VALUES (?, ?, ?, ?)",
        [user_id, post_id, body, int(time.time()), True],
    )
    return response_success()


@app.post("/like_comment")
def like_comment():
    if not request.json:
        raise Exception
    user_id = sessions.get(request.json["token"])
    comment_id: int = request.json["comment_id"]
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO comment_likes (user_id, comment_id, is_like) VALUES (?, ?, ?)",
        [user_id, comment_id, True],
    )
    con.commit()
    return response_success()


@app.post("/dislike_comment")
def dislike_comment():
    if not request.json:
        raise Exception
    user_id = sessions.get(request.json["token"])
    comment_id: int = request.json["comment_id"]
    con = sqlite3.connect(DB)
    con.execute(
        "INSERT INTO comment_likes (user_id, comment_id, is_like) VALUES (?, ?, ?)",
        [user_id, comment_id, False],
    )
    con.commit()
    return response_success()


@app.post("/unlike_comment")
def unlike_comment():
    if not request.json:
        raise Exception
    user_id = sessions.get(request.json["token"])
    comment_id: int = request.json["comment_id"]
    con = sqlite3.connect(DB)
    con.execute(
        "DELETE FROM comment_likes WHERE user_id = ? AND comment_id = ?",
        [user_id, comment_id],
    )
    con.commit()
    return response_success()


@app.get("/get_comment_like_count/<int:comment_id>")
def get_comment_like_count(comment_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM comment_likes WHERE comment_id = ? AND is_like = true",
        [comment_id],
    )
    _ = cur.fetchone()
    return response_success(count=_[0])


@app.get("/get_comment_dislike_count/<int:comment_id>")
def get_comment_dislike_count(comment_id: int):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM comment_likes WHERE comment_id = ? AND is_like = false",
        [comment_id],
    )
    _ = cur.fetchone()
    return response_success(count=_[0])
