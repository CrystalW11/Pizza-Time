# This file is used to initialize the Flask app and the Bcrypt object that will be used to hash passwords.
from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = "YabaDabaDoo"
load_dotenv()
