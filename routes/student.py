# Christiano Blairoy Fernandes
# 23f2004927
# 9 April 2026
# routes/student.py

# routes/student.py
from flask import Blueprint, g, redirect, render_template, request, session, url_for

from models import Student, db
from utils import login_required, role_required

student_bp = Blueprint("student", __name__)


@student_bp.before_request
def load_student():
    if "user_id" not in session :
        return  # no session, skip — login_required handles the redirect
    if session["role"] != "student":
        return redirect(url_for(f"{session['role']}.dashboard"))
    g.student = db.one_or_404(db.select(Student).filter_by(user_id=session["user_id"]))
    if g.student.account_status == "review" and request.endpoint != "student.dashboard":
        return redirect(url_for("student.dashboard"))
    elif g.student.account_status != "active" or g.student.user.status == "blacklisted":
        return redirect("/access-denied")


@student_bp.route("/dashboard")
@login_required
@role_required("student")
def dashboard():
    return render_template("student/dashboard.html", student=g.student)
