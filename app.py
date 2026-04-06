# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# /app.py

from flask import Flask

from config import Config
from models import db

myApp = Flask(__name__)
myApp.config.from_object(Config)
db.init_app(myApp)
