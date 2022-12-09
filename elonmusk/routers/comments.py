from sqlite3 import Connection
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .. import db
from ..lib import now
from .lib import failure, notauth, success, validate_session

router = APIRouter()


@router.get("/get_comments")
def get_comments(post_id: int, skip: int, count: int):
    _, cur = db.cursor()
    cur.execute(
        "SELECT id, user_id, body, likes, time FROM comments WHERE post_id = ? "
        "LIMIT ?, ?",
        [post_id, skip, count],
    )
    _ = cur.fetchall()
    return success(
        comments={
            n: {
                "id": i[0],
                "user_id": i[1],
                "body": i[2],
                "likes": i[3],
                "time": i[4],
            }
            for n, i in enumerate(_)
        }
    )


@router.get("/get_comment_count")
def get_comment_count(post_id: int):
    _, cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM comments WHERE post_id = ?", [post_id])
    return success(comment_count=cur.fetchone()[0])


@router.get("/get_comment")
def get_comment(id: int):
    _, cur = db.cursor()
    cur.execute(
        "SELECT user_id, post_id, body, likes, time FROM comments WHERE id = ?", [id]
    )
    _ = cur.fetchone()
    if not _:
        return failure("comment_does_not_exist")
    return success(
        user_id=_[0],
        post_id=_[1],
        body=_[2],
        likes=_[3],
        time=_[4],
    )


def calc_comment_like_count(con: Connection, id: int) -> None:
    con.execute(
        "UPDATE comments "
        "SET likes = (SELECT COUNT(*) FROM comment_likes WHERE comment_id = :id) "
        "WHERE post_id = :id",
        {"id": id},
    )


@router.post("/like_comment")
def like_comment(id: int, user_id: Optional[int] = Depends(validate_session)):
    if not user_id:
        return notauth()
    con = db.connect()
    con.execute(
        "INSERT INTO comment_likes (user_id, comment_id) VALUES (?, ?)", [user_id, id]
    )
    calc_comment_like_count(con, id)
    con.commit()
    return success()


@router.post("/unlike_comment")
def unlike_comment(id: int, user_id: Optional[int] = Depends(validate_session)):
    if not user_id:
        return notauth()
    con = db.connect()
    con.execute(
        "DELETE FROM comment_likes WHERE user_id = ? AND comment_id = ?", [user_id, id]
    )
    calc_comment_like_count(con, id)
    con.commit()
    return success()


class create_comment_T(BaseModel):
    post_id: int
    body: str


@router.post("/create_comment")
def create_comment(
    comment: create_comment_T, user_id: Optional[int] = Depends(validate_session)
):
    if not user_id:
        return notauth()
    con, cur = db.cursor()
    con.execute(
        "INSERT INTO comments (user_id, post_id, body, time) VALUES (?, ?, ?, ?)",
        [user_id, comment.post_id, comment.body, now()],
    )
    con.commit()
    cur.execute("SELECT id FROM comments WHERE rowid = last_insert_rowid()")
    return success(id=cur.fetchone()[0])
