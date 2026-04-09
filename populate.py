# Christiano Blairoy Fernandes
# 23f2004927
# seed.py — run from project root
# Usage:
#   python seed.py --create
#   python seed.py --destroy

import argparse
import json
import os
import sys
from datetime import datetime, timedelta, timezone

from werkzeug.security import generate_password_hash

SEED_MANIFEST = ".seed_manifest.json"


def load_manifest():
    if os.path.exists(SEED_MANIFEST):
        with open(SEED_MANIFEST) as f:
            return json.load(f)
    return {}


def save_manifest(manifest):
    with open(SEED_MANIFEST, "w") as f:
        json.dump(manifest, f, indent=2)


def create(app, db, User, Student, Company, Drive, Application):
    manifest = load_manifest()

    if manifest:
        print("Seed manifest already exists. Run --destroy first.")
        sys.exit(1)

    with app.app_context():
        manifest = {
            "users": [],
            "students": [],
            "companies": [],
            "drives": [],
            "applications": [],
        }

        # ── Users ─────────────────────────────────────────────────────────────

        raw_users = [
            # Students
            {"username": "seed_alice",   "email": "alice@seed.dev",   "role": "student"},
            {"username": "seed_bob",     "email": "bob@seed.dev",     "role": "student"},
            {"username": "seed_carol",   "email": "carol@seed.dev",   "role": "student"},
            {"username": "seed_dan",     "email": "dan@seed.dev",     "role": "student"},
            {"username": "seed_eve",     "email": "eve@seed.dev",     "role": "student"},
            # Companies
            {"username": "seed_techcorp",  "email": "hr@techcorp.seed",  "role": "company"},
            {"username": "seed_buildco",   "email": "hr@buildco.seed",   "role": "company"},
            {"username": "seed_datainc",   "email": "hr@datainc.seed",   "role": "company"},
        ]

        user_objs = []
        for u in raw_users:
            obj = User(
                username=u["username"],
                email=u["email"],
                password_hash=generate_password_hash("Seed@1234"),
                role=u["role"],
            )
            db.session.add(obj)
            user_objs.append(obj)

        db.session.flush()
        manifest["users"] = [u.id for u in user_objs]

        # ── Students ──────────────────────────────────────────────────────────

        student_data = [
            {"full_name": "Alice Fernandes", "department": "Computer Science",  "graduation_year": 2026, "cgpa": 9.1, "account_status": "active",      "gender": "Female"},
            {"full_name": "Bob Mascarenhas",  "department": "Electronics",       "graduation_year": 2026, "cgpa": 7.8, "account_status": "active",      "gender": "Male"},
            {"full_name": "Carol D'Souza",    "department": "Mechanical",        "graduation_year": 2027, "cgpa": 8.4, "account_status": "review",      "gender": "Female"},
            {"full_name": "Dan Rodrigues",    "department": "Computer Science",  "graduation_year": 2025, "cgpa": 6.5, "account_status": "deactivated", "gender": "Male"},
            {"full_name": "Eve Pereira",      "department": "Civil",             "graduation_year": 2026, "cgpa": 9.7, "account_status": "active",      "gender": "Female"},
        ]

        student_user_objs = [u for u in user_objs if u.role == "student"]
        student_objs = []
        for user, data in zip(student_user_objs, student_data):
            obj = Student(
                user_id=user.id,
                full_name=data["full_name"],
                department=data["department"],
                graduation_year=data["graduation_year"],
                cgpa=data["cgpa"],
                account_status=data["account_status"],
                gender=data["gender"],
                skills="Python, Communication, Teamwork",
            )
            db.session.add(obj)
            student_objs.append(obj)

        db.session.flush()
        manifest["students"] = [s.id for s in student_objs]

        # ── Companies ─────────────────────────────────────────────────────────

        company_data = [
            {"company_name": "Seed TechCorp",  "hr_contact": "Jane Doe",   "website": "https://techcorp.seed",  "approval_status": "approved"},
            {"company_name": "Seed BuildCo",   "hr_contact": "Mark Smith",  "website": "https://buildco.seed",   "approval_status": "pending"},
            {"company_name": "Seed DataInc",   "hr_contact": "Priya Nair",  "website": "https://datainc.seed",   "approval_status": "rejected"},
        ]

        company_user_objs = [u for u in user_objs if u.role == "company"]
        company_objs = []
        for user, data in zip(company_user_objs, company_data):
            obj = Company(
                user_id=user.id,
                company_name=data["company_name"],
                hr_contact=data["hr_contact"],
                website=data["website"],
                description=f"Seeded company — {data['company_name']}",
                approval_status=data["approval_status"],
            )
            db.session.add(obj)
            company_objs.append(obj)

        db.session.flush()
        manifest["companies"] = [c.id for c in company_objs]

        # ── Drives ────────────────────────────────────────────────────────────

        now = datetime.now(timezone.utc)

        drive_data = [
            {"company": company_objs[0], "job_title": "Backend Engineer",       "job_type": "Full-Time",   "ctc": "12 LPA",             "status": "approved", "days": 30},
            {"company": company_objs[0], "job_title": "ML Intern",              "job_type": "Internship",  "ctc": "25k/month",          "status": "approved", "days": 15},
            {"company": company_objs[0], "job_title": "DevOps Specialist",      "job_type": "Full-Time",   "ctc": "15 LPA",             "status": "closed",   "days": -5},
            {"company": company_objs[1], "job_title": "Site Engineer",          "job_type": "Full-Time",   "ctc": "8 LPA",              "status": "pending",  "days": 20},
            {"company": company_objs[2], "job_title": "Data Analyst",           "job_type": "Internship",  "ctc": "Performance Based",  "status": "pending",  "days": 10},
        ]

        drive_objs = []
        for d in drive_data:
            obj = Drive(
                company_id=d["company"].id,
                job_title=d["job_title"],
                job_description=f"Seeded drive for {d['job_title']}. Responsibilities include working on core projects.",
                job_type=d["job_type"],
                eligibility_criteria="Min CGPA 7.0, No active backlogs",
                status=d["status"],
                ctc=d["ctc"],
                location="Bangalore / Remote",
                application_deadline=now + timedelta(days=d["days"]),
            )
            db.session.add(obj)
            drive_objs.append(obj)

        db.session.flush()
        manifest["drives"] = [d.id for d in drive_objs]

        # ── Applications ──────────────────────────────────────────────────────

        # Only apply active students to approved drives
        active_students = [s for s in student_objs if s.account_status == "active"]
        approved_drives = [d for d in drive_objs if d.status == "approved"]

        app_data = [
            {"student": active_students[0], "drive": approved_drives[0], "approval_status": "shortlisted"},
            {"student": active_students[0], "drive": approved_drives[1], "approval_status": "applied"},
            {"student": active_students[1], "drive": approved_drives[0], "approval_status": "rejected"},
            {"student": active_students[2], "drive": approved_drives[1], "approval_status": "selected"},
        ]

        application_objs = []
        for a in app_data:
            obj = Application(
                student_id=a["student"].id,
                drive_id=a["drive"].id,
                approval_status=a["approval_status"],
            )
            db.session.add(obj)
            application_objs.append(obj)

        db.session.flush()
        manifest["applications"] = [a.id for a in application_objs]

        db.session.commit()
        save_manifest(manifest)

        print("✓ Seed complete.")
        print(f"  {len(manifest['users'])} users")
        print(f"  {len(manifest['students'])} students")
        print(f"  {len(manifest['companies'])} companies")
        print(f"  {len(manifest['drives'])} drives")
        print(f"  {len(manifest['applications'])} applications")
        print(f"  Manifest saved to {SEED_MANIFEST}")


def destroy(app, db, User, Student, Company, Drive, Application):
    manifest = load_manifest()

    if not manifest:
        print("No seed manifest found. Nothing to destroy.")
        sys.exit(1)

    with app.app_context():
        # Delete in reverse FK dependency order
        for app_id in manifest.get("applications", []):
            obj = db.session.get(Application, app_id)
            if obj:
                db.session.delete(obj)

        for drive_id in manifest.get("drives", []):
            obj = db.session.get(Drive, drive_id)
            if obj:
                db.session.delete(obj)

        for company_id in manifest.get("companies", []):
            obj = db.session.get(Company, company_id)
            if obj:
                db.session.delete(obj)

        for student_id in manifest.get("students", []):
            obj = db.session.get(Student, student_id)
            if obj:
                db.session.delete(obj)

        for user_id in manifest.get("users", []):
            obj = db.session.get(User, user_id)
            if obj:
                db.session.delete(obj)

        db.session.commit()
        os.remove(SEED_MANIFEST)

        print("✓ Seed data destroyed. Manifest removed.")


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Placement Portal DB Seeder")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--create",  action="store_true", help="Seed the database")
    group.add_argument("--destroy", action="store_true", help="Remove seeded data only")
    args = parser.parse_args()

    # Import app context here so the script is runnable from project root
    from app import myApp
    from models import Application, Company, Drive, Student, User, db

    if args.create:
        create(myApp, db, User, Student, Company, Drive, Application)
    elif args.destroy:
        destroy(myApp, db, User, Student, Company, Drive, Application)