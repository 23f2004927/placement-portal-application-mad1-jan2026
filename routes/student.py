# Christiano Blairoy Fernandes
# 23f2004927
# 9 April 2026
# routes/student.py

# routes/student.py
from werkzeug.utils import secure_filename
from models import Application
from models import Company
from models import Drive
from flask import Blueprint, g, redirect, render_template, request, session, url_for
import os
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
    company_id = request.args.get("company_id", "all")
    job_type = request.args.get("job_type", "all")
    search_query = request.args.get("searchQuery", "").strip()
    deadline_sort = request.args.get("deadline_sort", "asc")
    query = Drive.query.filter_by(status="approved")
    if company_id != "all":
        query = query.filter_by(company_id=company_id)
    if job_type != "all":
        query = query.filter_by(job_type=job_type)
    if search_query:
        query = query.filter(
            Drive.job_title.ilike(f"%{search_query}%") |
            Drive.location.ilike(f"%{search_query}%") |
            Drive.job_type.ilike(f"%{search_query}%")
        )

    if deadline_sort == "asc":
        query = query.order_by(Drive.application_deadline.asc())
    else:
        query = query.order_by(Drive.application_deadline.desc())

    available_drives = query.all()
    active_companies = Company.query.filter_by(approval_status="approved").all()
    applied_drive_ids = [app.drive_id for app in g.student.applications]

    return render_template("student/dashboard.html", student=g.student, available_drives=available_drives, activeCompanies=active_companies, applied_drive_ids=applied_drive_ids)




@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
@role_required("student")
def profile():
    if request.method == "POST":
        g.student.full_name = request.form.get("full_name")
        g.student.department = request.form.get("department")
        g.student.graduation_year = request.form.get("graduation_year")
        g.student.cgpa = request.form.get("cgpa")
        g.student.gender = request.form.get("gender")
        g.student.skills = request.form.get("skills")

        g.student.socials = {
            "linkedin": request.form.get("linkedin"),
            "github": request.form.get("github"),
        }
        resumefile = request.files.get("resume")

        if resumefile:
            
            safeFileName = secure_filename(f"{g.student.full_name}_{g.student.id}_{resumefile.filename}")
            save_dir = os.path.join("static", "uploads")
            os.makedirs(save_dir, exist_ok=True)
            resumefile.save(os.path.join(save_dir, safeFileName))
            g.student.resume_filename = safeFileName

        
        db.session.commit()
        return redirect(url_for("student.profile"))
    return render_template("student/profile.html", student=g.student)


@student_bp.route("/drive/<int:drive_id>" , methods=["GET", "POST"])
@login_required
@role_required("student")
def driveDetail(drive_id):
    drive = db.one_or_404(db.select(Drive).filter_by(id=drive_id))
    if not Application.query.filter_by(student_id=g.student.id, drive_id=drive_id).first():
        if request.method == "POST":
            new_application = Application(
                student_id=g.student.id,
                drive_id=drive_id,
            )
            db.session.add(new_application)
            db.session.commit()
            return redirect(url_for("student.dashboard"))
        return render_template("student/driveDetail.html", drive=drive, hasApplied=False)
    else:
        return render_template("student/driveDetail.html", drive=drive, hasApplied=True)
        



@student_bp.route("/applications")
@login_required
@role_required("student")
def applications():
    company_id = request.args.get("company_id", "all")
    job_type = request.args.get("job_type", "all")
    status = request.args.get("status", "all")
    search_query = request.args.get("searchQuery", "").strip()

    query = Application.query.join(Drive).filter(Application.student_id == g.student.id)

    if company_id != "all":
        query = query.filter(Company.id == company_id)
    if status != "all":
        match status:
            case "applied": 
                query = query.filter(Application.approval_status == status)
            case "shortlisted":
                query = query.filter(Application.approval_status == status)
            case "selected":
                query = query.filter(Application.approval_status == status)
            case "rejected":
                query = query.filter(Application.approval_status == status)
            case "hired":
                query = query.filter(Application.approval_status == status)
    if job_type != "all":
        query = query.filter(Drive.job_type == job_type)
    if search_query:
        query = query.filter(
            Drive.job_title.ilike(f"%{search_query}%") |
            Application.drive.location.ilike(f"%{search_query}%") |
            Application.drive.job_type.ilike(f"%{search_query}%")
        )

    myApplications = query.order_by(Application.applied_at.desc()).all()

    applied_companies = {app.drive.company for app in g.student.applications}

    return render_template("student/myApplications.html", myApplications=myApplications, applied_companies=applied_companies)



    