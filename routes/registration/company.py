# Christiano Blairoy Fernandes
# 23f2004927
# 8 April 2026
# routes/registration/company.py


from flask import Blueprint, flash, redirect, render_template, request, url_for
from werkzeug.security import generate_password_hash

from models import db
from models.company import Company
from models.user import User

company_reg = Blueprint("company_reg", __name__)


@company_reg.route("/register/company", methods=["GET", "POST"])
def registerCompany():
    if request.method == "GET":
        return render_template("auth/registerCompany.html")

    username = request.form.get("username", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    company_name = request.form.get("company_name", "").strip()
    hr_contact = request.form.get("hr_contact", "").strip()
    website = request.form.get("website", "").strip()
    description = request.form.get("description", "").strip()

    # Basic presence checks
    if not all([username, email, password, company_name]):
        return render_template(
            "auth/register_company.html",
            error="Username, email, password and company name are required.",
        )

    # Check for existing user
    if User.query.filter_by(username=username).first():
        return render_template(
            "auth/registerCompany.html", error="Username already taken."
        )

    if User.query.filter_by(email=email).first():
        return render_template(
            "auth/registerCompany.html", error="Email already registered."
        )

    # Check for existing company name
    if Company.query.filter_by(company_name=company_name).first():
        return render_template(
            "auth/registerCompany.html",
            error="A company with that name already exists.",
        )

    # Two-record insert
    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role="company",
    )
    db.session.add(new_user)
    db.session.flush()  # gets new_user.id without committing yet

    new_company = Company(
        user_id=new_user.id,
        company_name=company_name,
        hr_contact=hr_contact or None,
        website=website or None,
        description=description or None,
        approval_status="pending",
    )
    db.session.add(new_company)
    db.session.commit()

    flash(
        "Registration submitted. You can log in once your account is approved.", "info"
    )
    return redirect(url_for("auth.login"))
