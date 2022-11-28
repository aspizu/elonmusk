import secrets
from dataclasses import dataclass
from hashlib import blake2b

from .lib import now

SESSION_DURATION = 86400  # == 1 DAY


def is_username_valid(username: str) -> bool:
    return username.isalnum() and 3 <= len(username) <= 16


def is_password_valid(password: str) -> bool:
    return 8 <= len(password)


def is_avatar_valid(avatar: str) -> bool:
    return 1 <= len(avatar) <= 256


def is_email_valid(email: str) -> bool:
    return 1 <= len(email) <= 256


def is_bio_valid(bio: str) -> bool:
    return len(bio) <= 256


def hash_password(password: str, username: str) -> str:
    return blake2b((password + username).encode("UTF-8")).hexdigest()


def token() -> str:
    return secrets.token_urlsafe()


class SessionManager:
    @dataclass
    class Session:
        token: str
        username: str
        id: int
        creation_time: int

        def is_valid(self) -> bool:
            return now() < (self.creation_time + SESSION_DURATION)

    def __init__(self):
        self.sessions: dict[str, SessionManager.Session] = {}

    def create_session(self, username: str, id: int) -> "SessionManager.Session":
        session = SessionManager.Session(token(), username, id, now())
        self.sessions[session.token] = session
        return self.sessions[username]

    def get(self, token: str):
        try:
            session = self.sessions[token]
            if session.is_valid():
                return session
            else:
                self.sessions.pop(token)
        except KeyError:
            return


Sessions = SessionManager()
