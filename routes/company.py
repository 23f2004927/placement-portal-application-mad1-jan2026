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
from forms import CompanyProfileForm, DriveForm

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
    form = CompanyProfileForm(obj=g.company)

    if form.validate_on_submit():
        g.company.company_name = form.company_name.data
        g.company.industry     = form.industry.data
        g.company.hr_contact   = form.hr_contact.data
        g.company.website      = form.website.data
        g.company.description  = form.description.data
        db.session.commit()
        flash("Company profile updated successfully.", "success")
        return redirect(url_for('company.profile'))

    return render_template("company/companyProfile.html", company=g.company, form=form)


@company_bp.route("/drive/new", methods=["GET", "POST"])
@login_required
@role_required("company")
def createDrive():
    form = DriveForm()

    if form.validate_on_submit():
        try:
            newDrive = Drive(
                company_id=g.company.id,
                drive_name=form.drive_name.data,
                job_title=form.job_title.data,
                job_type=form.job_type.data,
                location=form.location.data,
                ctc=form.compensation.data,
                application_deadline=datetime.combine(
                    form.application_deadline.data, datetime.min.time()
                ),
                eligibility_criteria=form.eligibility_criteria.data,
                job_description=form.job_description.data,
            )
            db.session.add(newDrive)
            db.session.commit()
            flash("Drive created successfully.", "success")
            return redirect(url_for("company.dashboard"))
        except ValueError as e:
            flash(str(e), "error")

    # Render form on GET or if validation failed
    return render_template("company/createDrive.html", form=form)


@company_bp.route("/drive/<int:drive_id>", methods=["GET", "POST"])
@login_required
@role_required("company")
def manageDrive(drive_id):
    drive = db.one_or_404(db.select(Drive).filter_by(id=drive_id, company_id=g.company.id))
    form = DriveForm(obj=drive)

    if form.validate_on_submit():
        if drive.status == "closed":
            flash("Cannot edit a closed drive.", "error")
            return redirect(url_for("company.drives"))
        drive.ctc                  = form.compensation.data
        drive.application_deadline = datetime.combine(
            form.application_deadline.data, datetime.min.time()
        )
        drive.eligibility_criteria = form.eligibility_criteria.data
        drive.job_description      = form.job_description.data
        drive.status               = "pending"
        db.session.commit()
        flash("Drive updated successfully. Pending re-approval.", "success")
        return redirect(url_for("company.manageDrive", drive_id=drive.id))

    return render_template("company/driveView.html", drive=drive, form=form)


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
    VALID_TRANSITIONS = {
    "applied": {"shortlisted", "rejected"},
    "shortlisted": {"selected", "rejected"},
    "selected": {"hired"},
    "rejected": set(),
    "hired": set(),       
}
    application = db.one_or_404(db.select(Application).join(Drive).filter(Application.id==app_id, Drive.company_id==g.company.id))
    if request.method == "POST":

        application.rating = int(request.form.get("rating", 0))
        application.feedBack = request.form.get("feedback") or "Not Provided"
        current = application.approval_status
        new_status = request.form.get("approval_status")

        if new_status not in VALID_TRANSITIONS.get(current, set()):
            flash(f"Cannot move from '{current}' to '{new_status}'.", "error")
            return redirect(url_for("company.applicationDetail", app_id=application.id))
        application.approval_status = new_status
        
        if not 0 <= application.rating <= 5:
            flash("Rating must be between 0 and 5.", "error")
            return redirect(url_for("company.applicationDetail", app_id=application.id))

        db.session.commit()
        flash("Application updated successfully.", "success")
        return redirect(url_for("company.applicationDetail", app_id=application.id))
    
    return render_template("company/applicationDetail.html", application=application)
    
