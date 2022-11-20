import requests
from rich import print

API = "http://127.0.0.1:5000"

# r = requests.get(API + "/get_user/0")
# print(r.json())
#
# r = requests.post(
#     API + "/register",
#     json={
#         "username": "aspizu",
#         "email": "aspizu@protonmail.com",
#         "password": "12345678",
#         "bio": "",
#         "pfp": "https://avatars.githubusercontent.com/u/108279865",
#     },
# )
#
# print(r.json())

r = requests.get(API + "/get_user_follower_count/0")
print(r.json())
