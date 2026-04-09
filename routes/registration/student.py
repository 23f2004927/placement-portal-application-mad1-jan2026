# Christiano Blairoy Fernandes
# 23f2004927
# 8 April 2026
# routes/registration/student.py

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import generate_password_hash

from models import db
from models.student import Student
from models.user import User

student_reg = Blueprint("student_reg", __name__)


@student_reg.route("/register/student", methods=["GET", "POST"])
def registerStudent():
    if request.method == "GET":
        return render_template("auth/registerStudent.html")

    username = request.form.get("userName", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    full_name = request.form.get("fullName", "").strip()
    department = request.form.get("department", "").strip()
    graduation_year = request.form.get("graduationYear", "").strip()
    cgpa = request.form.get("cgpa", "").strip()

    if not all([username, email, password, full_name, department, graduation_year]):
        return render_template(
            "auth/registerStudent.html", error="All fields except CGPA are required."
        )

    if User.query.filter_by(username=username).first():
        return render_template(
            "auth/registerStudent.html", error="Username already taken."
        )

    if User.query.filter_by(email=email).first():
        return render_template(
            "auth/registerStudent.html", error="Email already registered."
        )

    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role="student",
    )
    db.session.add(new_user)
    db.session.flush()

    new_student = Student(
        user_id=new_user.id,
        full_name=full_name,
        department=department,
        graduation_year=int(graduation_year),
        cgpa=float(cgpa) if cgpa else None,
    )
    db.session.add(new_student)
    db.session.commit()

    # Auto-login
    session["user_id"] = new_user.id
    session["role"] = new_user.role
    session["username"] = new_user.username

    flash("Welcome! Your account has been created.", "success")
    return redirect(url_for("student.dashboard"))
