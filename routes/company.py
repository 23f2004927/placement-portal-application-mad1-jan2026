# Christiano Blairoy Fernandes
# 23f2004927
# 9 April 2026
# routes/company.py

from models import Student
from models import Application
from datetime import datetime

from flask import flash
from flask import request
from flask import url_for
from flask import Blueprint, g, render_template, session
from werkzeug.utils import redirect

from models import Company, db, Drive
from utils import login_required, role_required

company_bp = Blueprint("company", __name__)


@company_bp.before_request
def load_company():
    if "user_id" not in session:
        return  # no session, skip — login_required handles the redirect
    if session["role"] != "company":
        return redirect(url_for(f"{session['role']}.dashboard"))
    g.company = db.one_or_404(db.select(Company).filter_by(user_id=session["user_id"]))
    if g.company.approval_status != "approved" or g.company.user.status == "blacklisted":
        return redirect(url_for("auth.noAccess"))




@company_bp.route("/dashboard")
@login_required
@role_required("company")
def dashboard():
    allDrives = g.company.drives


    stats = {
        "total_drives": len(allDrives),
        "active_drives": sum(1 for d in allDrives if d.status == "approved"),
        "pending_drives": sum(1 for d in allDrives if d.status == "pending"),
        "closed_drives": sum(1 for d in allDrives if d.status == "closed"),
        "total_applications": 0,
        "shortlisted": 0,
        "selected": 0
    }

    for drive in allDrives:
        stats["total_applications"] += len(drive.applications)
        for app in drive.applications:
            if app.approval_status == "shortlisted":
                stats["shortlisted"] += 1
            elif app.approval_status == "selected":
                stats["selected"] += 1

    return render_template(
        "company/dashboard.html", 
        company=g.company, 
        drives=allDrives, 
        stats=stats
    )

@company_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("company")
def profile():
    if request.method == "POST":
        g.company.company_name = request.form.get("company_name")
        g.company.industry = request.form.get("industry")
        g.company.hr_contact = request.form.get("hr_contact")
        g.company.website = request.form.get("website")
        g.company.description = request.form.get("description")
        db.session.commit()
        flash("Company profile updated successfully.", "success")
        return redirect(url_for('company.profile'))

    else:
        return render_template(
        "company/companyProfile.html", 
        company=g.company
    )


@company_bp.route("/drive/new", methods=["GET", "POST"])
@login_required
@role_required("company")
def createDrive():
    if request.method == "POST":
        driveName = request.form.get("drive_name")
        jobTitle = request.form.get("job_title")
        jobType = request.form.get("job_type")
        location = request.form.get("location")
        compensation = request.form.get("compensation")
        applicationDeadline = datetime.strptime(request.form.get("application_deadline"), "%Y-%m-%d")
        eligibilityCriteria = request.form.get("eligibility_criteria")
        jobDescription = request.form.get("job_description")

        newDrive = Drive(
            company_id=g.company.id,
            drive_name=driveName,
            job_title=jobTitle,
            job_type=jobType,
            location=location,
            ctc=compensation,
            application_deadline=applicationDeadline,
            eligibility_criteria=eligibilityCriteria,
            job_description=jobDescription,
        )
        db.session.add(newDrive)
        db.session.commit()
        flash("Drive created successfully.", "success")
        return redirect(url_for("company.dashboard"))
    return render_template("company/createDrive.html")


@company_bp.route("/drive/<int:drive_id>", methods=["GET", "POST"])
@login_required
@role_required("company")
def manageDrive(drive_id):
    drive = db.one_or_404(db.select(Drive).filter_by(id=drive_id, company_id=g.company.id))

    if request.method == "POST":
        drive.ctc = request.form.get("compensation")
        drive.application_deadline = datetime.strptime(request.form.get("application_deadline"), "%Y-%m-%d")
        drive.eligibility_criteria = request.form.get("eligibility_criteria")
        drive.job_description = request.form.get("job_description")
        drive.status = "pending"
        db.session.commit()
        flash("Drive Updated successfully. Pending Approval.", "success")
        return redirect(url_for("company.manageDrive", drive_id=drive.id))
    return render_template("company/driveView.html", drive=drive)


@company_bp.route("/drives")
@login_required
@role_required("company")
def drives():
    search_query = request.args.get("searchQuery", "").strip()
    status_filter = request.args.get("status", "all").strip().lower()
    

    query = Drive.query.filter_by(company_id=g.company.id)
    filter_chips = []
    if status_filter != "all":
        query = query.filter(Drive.status == status_filter)
        filter_chips.append(f"STATUS: {status_filter.upper()}")

    if search_query:
        search_term = f"%{search_query}%"

        query = query.filter(
            db.or_(
                Drive.job_title.ilike(search_term),
                Drive.drive_name.ilike(search_term)
            )
        )
        filter_chips.append(f"SEARCH: '{search_query}'")


    filtered_drives = query.order_by(Drive.application_deadline.asc()).all()
    return render_template(
        "company/drives.html",
        drives=filtered_drives,
        filterChips=filter_chips
    )

@company_bp.route("/applications")
@login_required
@role_required("company")
def applications():
    search_query = request.args.get("searchQuery", "").strip()
    status_filter = request.args.get("status", "all").strip().lower()
    drive_filter = request.args.get("drive_id", "all").strip()

    query = Application.query.join(Drive).filter(Drive.company_id == g.company.id)
    filter_chips = []

    if drive_filter != "all":
        query = query.filter(Application.drive_id == drive_filter)
        drive_name = db.session.get(Drive, drive_filter).job_title
        filter_chips.append(f"DRIVE: {drive_name}")

    if status_filter != "all":
        query = query.filter(Application.approval_status == status_filter)
        filter_chips.append(f"STATUS: {status_filter.upper()}")

    if search_query:
        search_term = f"%{search_query}%"
        query = query.join(Student).filter(
            db.or_(
                Student.full_name.ilike(search_term),
                Student.department.ilike(search_term)
            )
        )
        filter_chips.append(f"SEARCH: '{search_query}'")

    applications = query.order_by(Application.applied_at.desc()).all()
    
    return render_template("company/applications.html", applications=applications, filterChips=filter_chips, company_drives=g.company.drives)



@company_bp.route("/applications/<int:app_id>", methods=["GET", "POST"])
@login_required
@role_required("company")
def applicationDetail(app_id):
    application = db.one_or_404(db.select(Application).join(Drive).filter(Application.id==app_id, Drive.company_id==g.company.id))
    if request.method == "POST":
        application.approval_status = request.form.get("approval_status")
        db.session.commit()
        flash("Application updated successfully.", "success")
        return redirect(url_for("company.applicationDetail", app_id=application.id))
    
    return render_template("company/applicationDetail.html", application=application)
    
