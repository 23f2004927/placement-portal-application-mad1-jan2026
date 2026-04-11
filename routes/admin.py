# Christiano Blairoy Fernandes
# 23f2004927
# 9 April 2026
# routes/admin.py

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import Application, Company, Drive, Student, db
from utils import login_required, role_required

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/dashboard")
@login_required
@role_required("admin")
def dashboard():
    stats = {
        "studentsCount": Student.query.count(),
        "companiesCount": Company.query.count(),
        "drivesCount": Drive.query.count(),
        "applicationsCount": Application.query.count(),
    }
    return render_template("admin/dashboard.html", stats=stats)


@admin_bp.route(
    "/companies",
    methods=[
        "GET",
    ],
)
@login_required
@role_required("admin")
def companies():

    query = Company.query

    search_term = request.args.get("searchQuery")

    if search_term:
        query = query.filter(Company.company_name.ilike(f"%{search_term}%"))

    queriedCompanies = query.all()
    return render_template("admin/companies.html", companies=queriedCompanies)


@admin_bp.route("/companies/<int:company_id>/action", methods=["POST"])
@login_required
@role_required("admin")
def company_action(company_id):
    company = db.get_or_404(Company, company_id)
    action = request.form.get("action")

    match action:
        case "approve":
            company.approval_status = "approved"
        case "reject":
            company.approval_status = "rejected"
        case "blacklist":
            company.user.status = "blacklisted"
            company.approval_status = "rejected" 

            for drive in company.drives:
                drive.status = "closed"
                for application in drive.applications:
                    application.approval_status = "rejected"
        case _:
            flash("Invalid action.", "warning")
            return redirect(url_for("admin.companies"))
    db.session.commit()
    return redirect(url_for("admin.companies"))


@admin_bp.route(
    "/students",
    methods=[
        "GET",
    ],
)
@login_required
@role_required("admin")
def students():
    query = Student.query
    batch = request.args.get("batch")
    cgpa = request.args.get("cgpa")
    search_term = request.args.get("searchQuery")

    if batch:
        query = query.filter_by(graduation_year=batch)
    if cgpa:
        query = query.filter(Student.cgpa >= float(cgpa))
    if search_term:
        query = query.filter(Student.full_name.ilike(f"%{search_term}%"))

    students = query.all()
    return render_template(
        "admin/students.html", students=students, batchFilter=batch, cgpaFilter=cgpa
    )


@admin_bp.route("/students/<int:student_id>/action", methods=["POST"])
@login_required
@role_required("admin")
def student_action(student_id):
    student = db.get_or_404(Student, student_id)
    action = request.form.get("action")

    match action:
        case "activate":
            student.account_status = "active"
        case "review":
            student.account_status = "review"
        case "blacklist":
            student.user.status = "blacklisted"
            for application in student.applications:
                application.approval_status = "rejected"
        case _:
            flash("Invalid action.", "warning")
            return redirect(url_for("admin.students"))
    db.session.commit()
    return redirect(url_for("admin.students"))


@admin_bp.route(
    "/drives",
    methods=[
        "GET",
    ],
)
@login_required
@role_required("admin")
def drives():
    all_page      = request.args.get('all_page', 1, type=int)
    pending_page  = request.args.get('pending_page', 1, type=int)
    approved_page = request.args.get('approved_page', 1, type=int)
    

    active_tab = request.args.get('tab', 'pending')
    query = Drive.query.join(Drive.company)
    search_term = request.args.get("searchQuery")
    if search_term:
        query = query.filter(
        Company.company_name.ilike(f"%{search_term}%") |
        Drive.job_title.ilike(f"%{search_term}%")
    )
    allDrives      = query.paginate(page=all_page, per_page=20)
    pendingDrives  = query.filter(Drive.status =="pending").paginate(page=pending_page, per_page=20)
    approvedDrives = query.filter(Drive.status=="approved").paginate(page=approved_page, per_page=20)
    return render_template(
        "admin/drives.html",
        allDrives=allDrives,
        pendingDrives=pendingDrives,
        approvedDrives=approvedDrives,
        activeTab=active_tab,
    )


@admin_bp.route(
    "/drives/<int:driveId>/action",
    methods=[
        "POST",
    ],
)
@login_required
@role_required("admin")
def driveAction(driveId):
    actionType = request.form.get("action")

    drive = db.get_or_404(Drive, driveId)
    match actionType:
        case "approve":
            drive.status = "approved"
            flash("Drive approved successfully.", "success")
        case "reject":
            drive.status = "rejected"
            flash("Drive rejected successfully.", "error")
        case "closed":
            drive.status = "closed"
            flash("Drive closed successfully.", "info")
        case "restore":
            if drive.company.user.status == "blacklisted":
                flash("Company is blacklisted.", "error")
            else:
                drive.status = "pending"
                flash("Drive restored successfully.", "info")
        case _:
            flash("Invalid action.", "warning")
            

    db.session.commit()
    return redirect(url_for("admin.drives"))



