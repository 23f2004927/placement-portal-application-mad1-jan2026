# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# /app.py

from flask import Flask, render_template

from config import Config
from models import db
from routes.auth import auth
from routes.registration import company_reg, student_reg

myApp = Flask(__name__)
myApp.config.from_object(Config)
myApp.register_blueprint(auth, url_prefix="/auth")
myApp.register_blueprint(company_reg, url_prefix="/auth")
myApp.register_blueprint(student_reg, url_prefix="/auth")

db.init_app(myApp)


@myApp.route("/")
def index():
    return render_template("/index.html")


if __name__ == "__main__":
    myApp.run(debug=True)
