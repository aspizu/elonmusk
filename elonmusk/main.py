from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import routers

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for i in routers:
    app.include_router(i)
