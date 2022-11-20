from flask import Flask
from flask_cors import CORS

from .sessions import Sessions

app = Flask(__name__)
CORS(app)
sessions = Sessions()
DB = "1.db"

from .api import comments  # noqa
from .api import posts  # noqa
from .api import users  # noqa
