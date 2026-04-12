# Christiano Blairoy Fernandes
# 23f2004927
# 8 April 2026
# routes/registration/company.py

from flask import Blueprint, flash, redirect, render_template, session, url_for
from werkzeug.security import generate_password_hash

from models import db
from models.company import Company
from models.user import User
from forms import CompanyRegistrationForm

company_reg = Blueprint("company_reg", __name__)


@company_reg.route("/register/company", methods=["GET", "POST"])
def registerCompany():
    form = CompanyRegistrationForm()

    if form.validate_on_submit():
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken.", "danger")
            return render_template("auth/registerCompany.html", form=form)

        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered.", "danger")
            return render_template("auth/registerCompany.html", form=form)

        if Company.query.filter_by(company_name=form.company_name.data).first():
            flash("A company with that name already exists.", "danger")
            return render_template("auth/registerCompany.html", form=form)

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=generate_password_hash(form.password.data),
            role="company",
        )
        db.session.add(new_user)
        db.session.flush()

        new_company = Company(
            user_id=new_user.id,
            company_name=form.company_name.data,
            hr_contact=form.hr_contact.data or None,
            website=form.website.data or None,
            description=form.description.data or None,
            approval_status="pending",
        )
        db.session.add(new_company)
        db.session.commit()

        flash("Registration submitted. You can log in once your account is approved.", "info")
        return redirect(url_for("auth.login"))

    # GET or validation failure
    return render_template("auth/registerCompany.html", form=form)
