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
