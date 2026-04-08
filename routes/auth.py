# Christiano Blairoy Fernandes
# 23f2004927
# 7 April 2026
# routes/auth.py

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash

from models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("auth/login.html")
    else:
        usernameQuery = request.form.get("username")
        passwordQuery = request.form.get("password")

        user = User.query.filter_by(username=usernameQuery).first()
        if user is not None and check_password_hash(
            user.password_hash, str(passwordQuery)
        ):
            session["user_id"] = user.id
            session["role"] = user.role
            session["username"] = user.username
            match session["role"]:
                # case "admin":
                #    return redirect(url_for("admin.dashboard"))
                # case "student":
                #    return redirect(url_for("student.dashboard"))
                # case "company":
                #    return redirect(url_for("company.dashboard"))
                #
                case "admin":
                    return render_template("index.html", role=session["role"])
                case "student":
                    return render_template("index.html", role=session["role"])
                case "company":
                    return render_template("index.html", role=session["role"])
        else:
            return render_template(
                "auth/login.html", error="Invalid username or password"
            )


@auth.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
