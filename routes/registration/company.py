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

    username = request.form.get("userName", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    company_name = request.form.get("companyName", "").strip()
    hr_contact = request.form.get("hrContact", "").strip()
    website = request.form.get("website", "").strip()
    description = request.form.get("description", "").strip()


    if not all([username, email, password, company_name]):
        flash("All fields are required", "error")
        return render_template(
            "auth/registerCompany.html",
        )


    if User.query.filter_by(username=username).first():
        flash("Username already taken.", "danger")
        return render_template(
            "auth/registerCompany.html", )

    if User.query.filter_by(email=email).first():
        flash("Email already registered.", "danger")
        return render_template("auth/registerCompany.html")


    if Company.query.filter_by(company_name=company_name).first():
        flash("A company with that name already exists.", "danger")
        return render_template(
            "auth/registerCompany.html",
        )


    new_user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role="company",
    )
    db.session.add(new_user)
    db.session.flush()  

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
