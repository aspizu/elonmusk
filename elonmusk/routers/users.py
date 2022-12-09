from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from .. import db
from ..lib import now
from ..sessions import (
    Sessions,
    hash_password,
    is_avatar_valid,
    is_bio_valid,
    is_email_valid,
    is_password_valid,
    is_username_valid,
)
from .lib import failure, notauth, success, validate_session

router = APIRouter()


@router.get("/get_user")
async def get_user(id: int):
    _, cur = db.cursor()
    cur.execute(
        "SELECT username, avatar, bio, time, rank FROM users WHERE id = ?", [id]
    )
    _ = cur.fetchone()
    if not _:
        return failure("user_does_not_exist")
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


@router.get("/get_user_followers")
async def get_user_followers(id: int, skip: int = 0, count: int = 10):
    _, cur = db.cursor()
    cur.execute(
        "SELECT follower_id FROM followers WHERE user_id = ? LIMIT ?, ?",
        [id, skip, count],
    )
    _ = cur.fetchall()
    if not _:
        return failure("no_followers")
    return success(followers=[i[0] for i in _])


class register_user_T(BaseModel):
    username: str
    email: str
    password: str
    avatar: Optional[str] = None
    bio: str


@router.post("/register")
async def register(user: register_user_T):
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
        [
            user.username,
            user.email,
            hash_password(user.password, user.username),
            user.avatar,
            user.bio,
            now(),
            0,
        ],
    )
    con.commit()
    return success()


class login_creds_T(BaseModel):
    username: str
    password: str


@router.post("/login")
async def login(creds: login_creds_T):
    _, cur = db.cursor()
    cur.execute("SELECT id, password FROM users WHERE username = ?", [creds.username])
    _ = cur.fetchone()
    if not _:
        return failure("user_does_not_exist")
    id: int = _[0]
    password: str = _[1]
    if hash_password(creds.password, creds.username) != password:
        return failure("incorrect_password")
    session = Sessions.create_session(creds.username, id)
    return success(token=session.token)


class update_user_data_T(BaseModel):
    email: Optional[str]
    avatar: Optional[str]
    bio: Optional[str]


@router.post("/update_user")
async def update_user(
    data: update_user_data_T, user_id: Optional[int] = Depends(validate_session)
):
    if not user_id:
        return notauth()

    con = db.connect()

    if data.email and not is_email_valid(data.email):
        return failure("invalid_email")
    if data.avatar and not is_avatar_valid(data.avatar):
        return failure("invalid_avatar")
    if data.bio and not is_bio_valid(data.bio):
        return failure("invalid_bio")

    sql = " ".join(
        [
            i
            for i in (
                data.email and "email = ?",
                data.avatar and "avatar = ?",
                data.bio and "bio = ?",
            )
            if i
        ]
    )

    if data.email:
        con.execute(
            f"UPDATE users SET {sql} WHERE id = ?",
            [*(i for i in (data.email, data.avatar, data.bio) if i), user_id],
        )

    con.commit()
    return success()


@router.post("/follow_user")
async def follow_user(id: int, user_id: Optional[int] = Depends(validate_session)):
    if not user_id:
        return notauth()
    con = db.connect()
    con.execute(
        "INSERT INTO followers (follower_id, user_id) VALUES (?, ?)", [user_id, id]
    )
    con.commit()
    return success()


@router.post("/unfollow_user")
async def unfollow_user(id: int, user_id: Optional[int] = Depends(validate_session)):
    if not user_id:
        return notauth()
    con = db.connect()
    con.execute(
        "DELETE FROM followers WHERE follower_id = ? AND user_id = ?", [user_id, id]
    )
    con.commit()
    return success()
