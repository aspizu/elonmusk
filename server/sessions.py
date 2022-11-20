import random


class Sessions:
    def __init__(self):
        self.sessions: dict[int, int] = {}

    def new(self, user_id: int) -> int:
        token = random.randint(0, 65536)
        self.sessions[token] = user_id
        return token

    def get(self, token: int) -> int:
        return self.sessions[token]
