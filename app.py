# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# /app.py

from flask import Flask, render_template

from config import Config
from models import db

# Import your new blueprints
from routes.admin import admin_bp
from routes.auth import auth
from routes.company import company_bp
from routes.registration import company_reg, student_reg
from routes.student import student_bp

myApp = Flask(__name__)
myApp.config.from_object(Config)

# Register existing auth blueprints
myApp.register_blueprint(auth, url_prefix="/auth")
myApp.register_blueprint(company_reg, url_prefix="/auth")
myApp.register_blueprint(student_reg, url_prefix="/auth")

# Register the new dashboard blueprints
myApp.register_blueprint(admin_bp, url_prefix="/admin")
myApp.register_blueprint(company_bp, url_prefix="/company")
myApp.register_blueprint(student_bp, url_prefix="/student")

db.init_app(myApp)


@myApp.route("/")
def index():
    return render_template("/index.html")


if __name__ == "__main__":
    myApp.run(debug=True)
