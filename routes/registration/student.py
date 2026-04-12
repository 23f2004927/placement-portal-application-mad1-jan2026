# Christiano Blairoy Fernandes
# 23f2004927
# 8 April 2026
# routes/registration/student.py

from flask import Blueprint, flash, redirect, render_template, session, url_for
from werkzeug.security import generate_password_hash

from models import db
from models.student import Student
from models.user import User
from forms import StudentRegistrationForm

student_reg = Blueprint("student_reg", __name__)


@student_reg.route("/register/student", methods=["GET", "POST"])
def registerStudent():
    form = StudentRegistrationForm()

    if form.validate_on_submit():
        # Uniqueness checks — WTForms validators don't query the DB, so we do it here
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken.", "error")
            return render_template("auth/registerStudent.html", form=form)

        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "error")
            return render_template("auth/registerStudent.html", form=form)

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role="student",
        )
        db.session.add(new_user)
        db.session.flush()

        new_student = Student(
            user_id=new_user.id,
            full_name=form.full_name.data,
            department=form.department.data,
            graduation_year=form.graduation_year.data,  # already int, no manual cast
            cgpa=form.cgpa.data,                        # already float or None
        )
        db.session.add(new_student)
        db.session.commit()

        session["user_id"]  = new_user.id
        session["role"]     = new_user.role
        session["username"] = new_user.username

        flash("Welcome! Your account has been created.", "success")
        return redirect(url_for("student.dashboard"))

    # GET or validation failure — render with errors
    return render_template("auth/registerStudent.html", form=form)
