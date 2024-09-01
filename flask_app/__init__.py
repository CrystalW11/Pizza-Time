from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "YabaDabaDoo"
load_dotenv()
