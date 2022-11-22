from fastapi import APIRouter
from pydantic import BaseModel

from .. import db
from ..sessions import (
    is_avatar_valid,
    is_bio_valid,
    is_email_valid,
    is_password_valid,
    is_username_valid,
)
from .lib import failure, success

router = APIRouter()


@router.get("/get_user")
async def get_user(id: int):
    _, cur = db.cursor()
    cur.execute(
        "SELECT username, avatar, bio, time, rank FROM users WHERE id = ?", [id]
    )
    _ = cur.fetchone()
    if not _:
        return {"error": "user_does_not_exist"}
    return success(
        username=_[0],
        avatar=_[1],
        bio=_[2],
        time=_[3],
        rank=_[4],
    )


@router.get("/get_user_follower_count")
async def get_user_follower_count(id: int):
    _, cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM followers WHERE user_id = ?", [id])
    _ = cur.fetchone()
    return success(follower_count=_[0])


class _T(BaseModel):
    username: str
    email: str
    password: str
    avatar: str | None = None
    bio: str


@router.post("/register")
async def register(user: _T):
    con, cur = db.cursor()
    if not is_username_valid(user.username):
        return failure("invalid_username")
    if not is_email_valid(user.email):
        return failure("invalid_email")
    if not is_password_valid(user.password):
        return failure("invalid_password")
    if not user.avatar or not is_avatar_valid(user.avatar):
        user.avatar = f"https://ui-avatars.com/api/?name={user.username}"
    if not is_bio_valid(user.bio):
        return failure("invalid_bio")
    cur.execute("SELECT id FROM users WHERE username = ?", [user.username])
    if cur.fetchone() is not None:
        return failure("username_taken")
    con.execute(
        "INSERT INTO users (username, email, password, avatar, bio, time, rank)"
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [user.username, user.email, user.password, user.avatar, user.bio, 0, 0],
    )
    con.commit()
    return success()
