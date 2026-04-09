# Christiano Blairoy Fernandes
# 23f2004927
# 9 April 2026
# routes/company.py

# routes/company.py
from flask import url_for
from flask import Blueprint, g, render_template, session
from werkzeug.utils import redirect

from models import Company, db
from utils import login_required, role_required

company_bp = Blueprint("company", __name__)


@company_bp.before_request
def load_company():
    if "user_id" not in session:
        return  # no session, skip — login_required handles the redirect
    if session["role"] != "company":
        return redirect(url_for(f"{session['role']}.dashboard"))
    g.company = db.one_or_404(db.select(Company).filter_by(user_id=session["user_id"]))
    if g.company.approval_status != "approved":
        return redirect(url_for("auth.noAccess"))


@company_bp.route("/access-denied")
@login_required
def noAccess():
    return render_template("company/noAccess.html", company=g.company)


@company_bp.route("/dashboard")
@login_required
@role_required("company")
def dashboard():
    # Temporary dummy data to render the UI

    return render_template("company/dashboard.html", company=g.company)


@company_bp.route("/drive/new", methods=["GET", "POST"])
@login_required
@role_required("company")
def create_drive():
    # We will handle the POST request (saving to DB) later.
    # For now, just render the form.
    return render_template("company/createDrive.html")
