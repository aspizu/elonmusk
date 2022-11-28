from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .. import db
from ..lib import now
from .lib import failure, notauth, success, validate_session

router = APIRouter()


@router.get("/get_posts")
def get_posts(skip: int, count: int):
    _, cur = db.cursor()
    cur.execute("SELECT id, user_id, body, time FROM posts LIMIT ?, ?", [skip, count])
    _ = cur.fetchall()
    return success(
        posts={
            i[0]: {"id": i[1], "user_id": i[2], "body": i[3], "time": i[4]} for i in _
        }
    )


@router.get("/get_post")
def get_post(id: int):
    _, cur = db.cursor()
    cur.execute("SELECT user_id, body, time FROM posts WHERE id = ?", [id])
    _ = cur.fetchone()
    if not _:
        return failure("post_does_not_exist")
    return success(
        user_id=_[0],
        body=_[1],
        time=_[2],
    )


@router.get("/get_post_like_count")
def get_post_like_count(id: int):
    _, cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM post_likes WHERE post_id = ?", [id])
    _ = cur.fetchone()
    return success(follower_count=_[0])


@router.post("/like_post")
def like_post(id: int, user_id: Optional[int] = Depends(validate_session)):
    if not user_id:
        return notauth()
    con = db.connect()
    con.execute(
        "INSERT INTO post_likes (user_id, post_id) VALUES (?, ?)", [user_id, id]
    )


@router.post("/unlike_post")
def unlike_post(id: int, user_id: Optional[int] = Depends(validate_session)):
    if not user_id:
        return notauth()
    con = db.connect()
    con.execute(
        "DELETE FROM post_likes WHERE user_id = ? AND post_id = ?", [user_id, id]
    )


class create_post_T(BaseModel):
    body: str


@router.post("/create_post")
def create_post(
    post: create_post_T, user_id: Optional[int] = Depends(validate_session)
):
    if not user_id:
        return notauth()
    con, cur = db.cursor()
    con.execute(
        "INSERT INTO posts (user_id, body, time) VALUES (?, ?, ?)",
        [user_id, post.body, now()],
    )
    con.commit()
    cur.execute("SELECT id FROM posts WHERE rowid = last_insert_rowid()")
    return success(id=cur.fetchone()[0])
