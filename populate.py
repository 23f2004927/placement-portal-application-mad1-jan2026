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
from datetime import datetime, timedelta

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

        now = datetime.utcnow()

        # ── Users ─────────────────────────────────────────────────────────────
        # User.status:  "active" | "blacklisted"
        # User.role:    "admin"  | "student" | "company"
        #
        # Blacklisting a company is done here on User, not on Company.approval_status
        # (Company.approval_status only carries: pending / approved / rejected)

        raw_users = [
            # ── Students ──────────────────────────────────────────────────────
            {"username": "seed_alice",    "email": "alice@seed.dev",      "role": "student", "status": "active"},
            {"username": "seed_bob",      "email": "bob@seed.dev",        "role": "student", "status": "active"},
            {"username": "seed_carol",    "email": "carol@seed.dev",      "role": "student", "status": "active"},
            {"username": "seed_dan",      "email": "dan@seed.dev",        "role": "student", "status": "blacklisted"},   # blacklisted student
            {"username": "seed_eve",      "email": "eve@seed.dev",        "role": "student", "status": "active"},
            {"username": "seed_frank",    "email": "frank@seed.dev",      "role": "student", "status": "active"},
            {"username": "seed_grace",    "email": "grace@seed.dev",      "role": "student", "status": "active"},
            {"username": "seed_henry",    "email": "henry@seed.dev",      "role": "student", "status": "active"},
            {"username": "seed_isla",     "email": "isla@seed.dev",       "role": "student", "status": "active"},
            {"username": "seed_jay",      "email": "jay@seed.dev",        "role": "student", "status": "active"},
            # ── Companies ─────────────────────────────────────────────────────
            {"username": "seed_techcorp", "email": "hr@techcorp.seed",    "role": "company", "status": "active"},
            {"username": "seed_buildco",  "email": "hr@buildco.seed",     "role": "company", "status": "active"},
            {"username": "seed_datainc",  "email": "hr@datainc.seed",     "role": "company", "status": "active"},
            {"username": "seed_finedge",  "email": "hr@finedge.seed",     "role": "company", "status": "active"},
            {"username": "seed_healthai", "email": "hr@healthai.seed",    "role": "company", "status": "active"},
            {"username": "seed_rogue",    "email": "hr@rogue.seed",       "role": "company", "status": "blacklisted"},  # blacklisted company (User-level)
        ]

        user_objs = []
        for u in raw_users:
            obj = User(
                username=u["username"],
                email=u["email"],
                password_hash=generate_password_hash("Seed@1234"),
                role=u["role"],
                status=u["status"],
            )
            db.session.add(obj)
            user_objs.append(obj)

        db.session.flush()
        manifest["users"] = [u.id for u in user_objs]

        # ── Students ──────────────────────────────────────────────────────────
        # account_status: "active" | "review" | "deactivated"
        #   "active"      — fully onboarded, can apply
        #   "review"      — profile incomplete / under review, cannot apply
        #   "deactivated" — account turned off (self-requested or admin action)
        #
        # is_blacklisted is NOT on Student — check student.user.status == "blacklisted"
        # socials is a nullable JSON field

        student_data = [
            {
                "full_name": "Alice Fernandes",
                "department": "Computer Science", "graduation_year": 2026,
                "cgpa": 9.1, "account_status": "active", "gender": "Female",
                "skills": "Python, Django, Machine Learning, SQL",
                "socials": {"linkedin": "https://linkedin.com/in/alice-f", "github": "https://github.com/alice-f"},
            },
            {
                "full_name": "Bob Mascarenhas",
                "department": "Electronics", "graduation_year": 2026,
                "cgpa": 7.8, "account_status": "active", "gender": "Male",
                "skills": "Embedded C, PCB Design, MATLAB, IoT",
                "socials": {"linkedin": "https://linkedin.com/in/bob-m"},
            },
            {
                "full_name": "Carol D'Souza",
                "department": "Mechanical", "graduation_year": 2027,
                "cgpa": 8.4, "account_status": "review", "gender": "Female",
                "skills": "AutoCAD, SolidWorks, Thermodynamics",
                "socials": None,
            },
            {
                "full_name": "Dan Rodrigues",           # user is blacklisted
                "department": "Computer Science", "graduation_year": 2025,
                "cgpa": 6.5, "account_status": "review", "gender": "Male",
                "skills": "Java, Android, Firebase",
                "socials": {"github": "https://github.com/dan-r"},
            },
            {
                "full_name": "Eve Pereira",
                "department": "Civil", "graduation_year": 2026,
                "cgpa": 9.7, "account_status": "active", "gender": "Female",
                "skills": "Structural Analysis, AutoCAD, STAAD Pro",
                "socials": {"linkedin": "https://linkedin.com/in/eve-p"},
            },
            {
                "full_name": "Frank Almeida",
                "department": "Information Technology", "graduation_year": 2026,
                "cgpa": 8.0, "account_status": "active", "gender": "Male",
                "skills": "React, Node.js, PostgreSQL, Docker",
                "socials": {"linkedin": "https://linkedin.com/in/frank-a", "github": "https://github.com/frank-a"},
            },
            {
                "full_name": "Grace Mathews",
                "department": "Computer Science", "graduation_year": 2027,
                "cgpa": 9.3, "account_status": "active", "gender": "Female",
                "skills": "Data Science, TensorFlow, Pandas, Tableau",
                "socials": {"linkedin": "https://linkedin.com/in/grace-m", "github": "https://github.com/grace-m"},
            },
            {
                "full_name": "Henry Costa",
                "department": "Electrical", "graduation_year": 2026,
                "cgpa": 7.2, "account_status": "active", "gender": "Male",
                "skills": "Power Systems, PLC Programming, SCADA",
                "socials": None,
            },
            {
                "full_name": "Isla Noronha",           # account deactivated (third status value)
                "department": "Information Technology", "graduation_year": 2025,
                "cgpa": 8.8, "account_status": "deactivated", "gender": "Female",
                "skills": "Cybersecurity, Penetration Testing, Linux",
                "socials": {"github": "https://github.com/isla-n"},
            },
            {
                "full_name": "Jay Pinto",
                "department": "Computer Science", "graduation_year": 2026,
                "cgpa": 7.5, "account_status": "active", "gender": "Prefer Not To Say",
                "skills": "Go, Kubernetes, Cloud (AWS), CI/CD",
                "socials": {"linkedin": "https://linkedin.com/in/jay-p"},
            },
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
                skills=data["skills"],
                socials=data["socials"],
            )
            db.session.add(obj)
            student_objs.append(obj)

        db.session.flush()
        manifest["students"] = [s.id for s in student_objs]

        # ── Companies ─────────────────────────────────────────────────────────
        # approval_status: "pending" | "approved" | "rejected"
        # Blacklisted company is handled at User.status level (see raw_users above)
        # The "rejected" and "blacklisted-user" cases are both seeded for completeness

        company_data = [
            {
                "company_name": "Seed TechCorp",
                "hr_contact": "Jane Doe",   "website": "https://techcorp.seed",
                "industry": "Software & IT", "approval_status": "approved",
                "description": "A product-first software company building developer tools.",
            },
            {
                "company_name": "Seed BuildCo",
                "hr_contact": "Mark Smith", "website": "https://buildco.seed",
                "industry": "Construction & Infrastructure", "approval_status": "pending",
                "description": "Infrastructure and civil construction firm across South India.",
            },
            {
                "company_name": "Seed DataInc",
                "hr_contact": "Priya Nair", "website": "https://datainc.seed",
                "industry": "Data Analytics", "approval_status": "rejected",
                "description": "Analytics and BI solutions for enterprise clients.",
            },
            {
                "company_name": "Seed FinEdge",
                "hr_contact": "Rohan Mehta", "website": "https://finedge.seed",
                "industry": "Fintech", "approval_status": "approved",
                "description": "Payments and lending platform serving SMEs.",
            },
            {
                "company_name": "Seed HealthAI",
                "hr_contact": "Dr. Shreya Iyer", "website": "https://healthai.seed",
                "industry": "Healthcare & AI", "approval_status": "approved",
                "description": "AI-assisted diagnostic tools for hospitals and clinics.",
            },
            {
                "company_name": "Seed RogueTech",       # User is blacklisted
                "hr_contact": "Unknown",   "website": "https://rogue.seed",
                "industry": "Miscellaneous", "approval_status": "approved",  # was approved before blacklist
                "description": "Flagged company — access revoked at User level.",
            },
        ]

        company_user_objs = [u for u in user_objs if u.role == "company"]
        company_objs = []
        for user, data in zip(company_user_objs, company_data):
            obj = Company(
                user_id=user.id,
                company_name=data["company_name"],
                hr_contact=data["hr_contact"],
                website=data["website"],
                industry=data["industry"],
                description=data["description"],
                approval_status=data["approval_status"],
            )
            db.session.add(obj)
            company_objs.append(obj)

        db.session.flush()
        manifest["companies"] = [c.id for c in company_objs]

        # Convenience aliases
        techcorp  = company_objs[0]   # approved
        buildco   = company_objs[1]   # pending
        datainc   = company_objs[2]   # rejected
        finedge   = company_objs[3]   # approved
        healthai  = company_objs[4]   # approved
        rogue     = company_objs[5]   # approved (but user blacklisted)

        # ── Drives ────────────────────────────────────────────────────────────
        # status: "pending" | "approved" | "rejected" | "closed"
        # Only approved companies should have approved drives.
        # Rogue's drives are closed (simulating the cascade when a company is blacklisted).
        # pending/rejected companies can still have pending drives (submitted before decision).

        drive_data = [
            # TechCorp (approved) ─────────────────────────────────────────────
            {
                "company": techcorp, "drive_name": "TechCorp SWE 2026",
                "job_title": "Backend Engineer", "job_type": "Full-Time",
                "job_description": "Design and maintain scalable REST APIs using Python and FastAPI. Work with distributed systems and cloud infrastructure.",
                "eligibility_criteria": "Min CGPA 7.5 | CS / IT / ECE | 2025 or 2026 batch",
                "ctc": "12 LPA", "location": "Bangalore", "status": "approved", "days": 30,
            },
            {
                "company": techcorp, "drive_name": "TechCorp ML Internship",
                "job_title": "ML Intern", "job_type": "Internship",
                "job_description": "Assist the ML team in model training, evaluation, and deployment pipelines. Familiarity with PyTorch or TensorFlow preferred.",
                "eligibility_criteria": "Min CGPA 7.0 | All branches | 2026 or 2027 batch",
                "ctc": "25k/month", "location": "Remote", "status": "approved", "days": 15,
            },
            {
                "company": techcorp, "drive_name": "TechCorp DevOps 2025",
                "job_title": "DevOps Specialist", "job_type": "Full-Time",
                "job_description": "Manage CI/CD pipelines, container orchestration, and cloud infrastructure. Experience with Kubernetes and Terraform is a plus.",
                "eligibility_criteria": "Min CGPA 7.0 | CS / IT | 2025 batch",
                "ctc": "15 LPA", "location": "Hyderabad", "status": "closed", "days": 1,  # closed by company action; deadline value is moot
            },
            {
                "company": techcorp, "drive_name": "TechCorp Frontend React",
                "job_title": "Frontend Developer", "job_type": "Full-Time",
                "job_description": "Build and maintain user-facing features using React and TypeScript. Collaborate with design and backend teams.",
                "eligibility_criteria": "Min CGPA 6.5 | CS / IT | 2026 batch",
                "ctc": "10 LPA", "location": "Pune", "status": "pending", "days": 25,
            },
            # FinEdge (approved) ──────────────────────────────────────────────
            {
                "company": finedge, "drive_name": "FinEdge SDE 2026",
                "job_title": "Software Development Engineer", "job_type": "Full-Time",
                "job_description": "Build core payment and reconciliation services. Work with high-throughput transaction systems.",
                "eligibility_criteria": "Min CGPA 8.0 | CS / IT | 2026 batch",
                "ctc": "14 LPA", "location": "Mumbai", "status": "approved", "days": 20,
            },
            {
                "company": finedge, "drive_name": "FinEdge Data Intern",
                "job_title": "Data Engineering Intern", "job_type": "Internship",
                "job_description": "Work on ETL pipelines, data warehousing, and reporting dashboards using Spark and Airflow.",
                "eligibility_criteria": "Min CGPA 7.5 | CS / IT / Math | All batches",
                "ctc": "20k/month", "location": "Remote", "status": "approved", "days": 12,
            },
            {
                "company": finedge, "drive_name": "FinEdge QA Analyst",
                "job_title": "QA Analyst", "job_type": "Full-Time",
                "job_description": "Own the automated testing strategy across web and mobile products. Write Selenium and Appium test suites.",
                "eligibility_criteria": "Min CGPA 7.0 | Any branch | 2025 or 2026 batch",
                "ctc": "8 LPA", "location": "Mumbai", "status": "rejected", "days": 18,  # rejected by admin
            },
            # HealthAI (approved) ─────────────────────────────────────────────
            {
                "company": healthai, "drive_name": "HealthAI Research Intern",
                "job_title": "AI Research Intern", "job_type": "Internship",
                "job_description": "Assist in developing computer vision models for medical imaging. Exposure to DICOM data and clinical workflows.",
                "eligibility_criteria": "Min CGPA 8.5 | CS / IT | 2026 or 2027 batch",
                "ctc": "30k/month", "location": "Chennai", "status": "approved", "days": 22,
            },
            {
                "company": healthai, "drive_name": "HealthAI Full Stack",
                "job_title": "Full Stack Engineer", "job_type": "Full-Time",
                "job_description": "Build patient-facing and clinician-facing web portals. Django + React stack.",
                "eligibility_criteria": "Min CGPA 7.5 | CS / IT | 2026 batch",
                "ctc": "11 LPA", "location": "Bangalore", "status": "pending", "days": 35,
            },
            # BuildCo (pending approval — their drives are also pending) ───────
            {
                "company": buildco, "drive_name": "BuildCo Site Engineer Drive",
                "job_title": "Site Engineer", "job_type": "Full-Time",
                "job_description": "Supervise construction activities on-site, manage contractors, and ensure quality compliance.",
                "eligibility_criteria": "Min CGPA 6.0 | Civil / Mechanical | 2025 or 2026 batch",
                "ctc": "8 LPA", "location": "Goa / Mangalore", "status": "pending", "days": 20,
            },
            # DataInc (rejected company — drives should also be inaccessible) ─
            {
                "company": datainc, "drive_name": "DataInc Analyst Intake",
                "job_title": "Data Analyst", "job_type": "Internship",
                "job_description": "Work with business analysts to build dashboards and reporting pipelines.",
                "eligibility_criteria": "Min CGPA 6.5 | Any branch | 2026 batch",
                "ctc": "Performance Based", "location": "Remote", "status": "pending", "days": 10,
            },
            # RogueTech (user blacklisted — drives closed via cascade) ─────────
            {
                "company": rogue, "drive_name": "Rogue Internship",
                "job_title": "Software Intern", "job_type": "Internship",
                "job_description": "General software internship role.",
                "eligibility_criteria": "Min CGPA 6.0 | Any branch",
                "ctc": "10k/month", "location": "Remote", "status": "closed", "days": 1,  # closed by blacklist cascade; deadline value is moot
            },
        ]

        drive_objs = []
        for d in drive_data:
            obj = Drive(
                company_id=d["company"].id,
                drive_name=d["drive_name"],
                job_title=d["job_title"],
                job_description=d["job_description"],
                job_type=d["job_type"],
                eligibility_criteria=d["eligibility_criteria"],
                status=d["status"],
                ctc=d["ctc"],
                location=d["location"],
                application_deadline=now + timedelta(days=d["days"]),
            )
            db.session.add(obj)
            drive_objs.append(obj)

        db.session.flush()
        manifest["drives"] = [d.id for d in drive_objs]

        # Convenience: approved drives only (students can only apply to these)
        approved_drives = [d for d in drive_objs if d.status == "approved"]
        # approved_drives indices:
        #   0 → TechCorp Backend Engineer
        #   1 → TechCorp ML Intern
        #   2 → FinEdge SDE
        #   3 → FinEdge Data Intern
        #   4 → HealthAI Research Intern

        # ── Students eligible to apply ────────────────────────────────────────
        # Must be: user.status == "active" AND account_status == "active"
        eligible = [
            s for s in student_objs
            if s.account_status == "active" and s.user.status == "active"
        ]
        # eligible: Alice(0), Bob(1), Eve(4), Frank(5), Grace(6), Henry(7), Jay(9)

        alice  = eligible[0]   # CS, 9.1 CGPA
        bob    = eligible[1]   # Electronics, 7.8 CGPA
        eve    = eligible[2]   # Civil, 9.7 CGPA
        frank  = eligible[3]   # IT, 8.0 CGPA
        grace  = eligible[4]   # CS, 9.3 CGPA
        henry  = eligible[5]   # Electrical, 7.2 CGPA
        jay    = eligible[6]   # CS, 7.5 CGPA

        tc_backend   = approved_drives[0]   # TechCorp Backend Engineer
        tc_ml        = approved_drives[1]   # TechCorp ML Intern
        fe_sde       = approved_drives[2]   # FinEdge SDE
        fe_data      = approved_drives[3]   # FinEdge Data Intern
        hai_research = approved_drives[4]   # HealthAI Research Intern

        # ── Applications ──────────────────────────────────────────────────────
        # approval_status: "applied" | "shortlisted" | "selected" | "rejected" | "hired"
        # rating: 0–5 (CheckConstraint enforced at DB level)
        # UniqueConstraint on (student_id, drive_id) — no duplicates allowed

        app_data = [
            # TechCorp Backend Engineer ────────────────────────────────────────
            {   # Alice: shortlisted — strong candidate
                "student": alice, "drive": tc_backend,
                "approval_status": "shortlisted", "rating": 4,
                "feedBack": "Excellent problem-solving. Invited for technical round.",
            },
            {   # Bob: rejected — CGPA below threshold for this role
                "student": bob, "drive": tc_backend,
                "approval_status": "rejected", "rating": 2,
                "feedBack": "CGPA is below the internal cutoff for this role.",
            },
            {   # Frank: selected
                "student": frank, "drive": tc_backend,
                "approval_status": "selected", "rating": 5,
                "feedBack": "Strong full-stack background. Cleared all rounds.",
            },
            {   # Jay: applied — no decision yet
                "student": jay, "drive": tc_backend,
                "approval_status": "applied", "rating": 0,
                "feedBack": "Not Provided",
            },
            {   # Grace: hired — completed onboarding
                "student": grace, "drive": tc_backend,
                "approval_status": "hired", "rating": 5,
                "feedBack": "Offer accepted. Joining confirmed for July 2026.",
            },
            # TechCorp ML Intern ───────────────────────────────────────────────
            {   # Alice: selected (also applied here — different drive, valid)
                "student": alice, "drive": tc_ml,
                "approval_status": "selected", "rating": 5,
                "feedBack": "Impressive ML project portfolio.",
            },
            {   # Grace: shortlisted
                "student": grace, "drive": tc_ml,
                "approval_status": "shortlisted", "rating": 4,
                "feedBack": "Strong academic background in data science.",
            },
            {   # Henry: applied
                "student": henry, "drive": tc_ml,
                "approval_status": "applied", "rating": 0,
                "feedBack": "Not Provided",
            },
            # FinEdge SDE ─────────────────────────────────────────────────────
            {   # Frank: hired (dual offer scenario — shows hired status)
                "student": frank, "drive": fe_sde,
                "approval_status": "hired", "rating": 5,
                "feedBack": "Accepted FinEdge offer. Joining date confirmed.",
            },
            {   # Grace: rejected — accepted TechCorp instead
                "student": grace, "drive": fe_sde,
                "approval_status": "rejected", "rating": 3,
                "feedBack": "Candidate declined after receiving another offer.",
            },
            {   # Jay: shortlisted
                "student": jay, "drive": fe_sde,
                "approval_status": "shortlisted", "rating": 3,
                "feedBack": "Good understanding of backend systems.",
            },
            # FinEdge Data Intern ──────────────────────────────────────────────
            {   # Alice: applied
                "student": alice, "drive": fe_data,
                "approval_status": "applied", "rating": 0,
                "feedBack": "Not Provided",
            },
            {   # Eve: applied (Civil — company allows all branches for intern)
                "student": eve, "drive": fe_data,
                "approval_status": "applied", "rating": 0,
                "feedBack": "Not Provided",
            },
            # HealthAI Research Intern ────────────────────────────────────────
            {   # Grace: selected — CGPA 9.3 meets the 8.5 cutoff
                "student": grace, "drive": hai_research,
                "approval_status": "selected", "rating": 5,
                "feedBack": "Top candidate. Research experience aligns perfectly.",
            },
            {   # Alice: shortlisted — CGPA 9.1 meets cutoff
                "student": alice, "drive": hai_research,
                "approval_status": "shortlisted", "rating": 4,
                "feedBack": "Strong profile. Pending final interview.",
            },
            {   # Jay: rejected — CGPA 7.5 below 8.5 cutoff
                "student": jay, "drive": hai_research,
                "approval_status": "rejected", "rating": 1,
                "feedBack": "Does not meet the minimum CGPA requirement for this role.",
            },
        ]

        application_objs = []
        for a in app_data:
            obj = Application(
                student_id=a["student"].id,
                drive_id=a["drive"].id,
                approval_status=a["approval_status"],
                rating=a["rating"],
                feedBack=a["feedBack"],
            )
            db.session.add(obj)
            application_objs.append(obj)

        db.session.flush()
        manifest["applications"] = [a.id for a in application_objs]

        db.session.commit()
        save_manifest(manifest)

        # ── Summary ───────────────────────────────────────────────────────────
        print("✓ Seed complete.")
        print(f"  {len(manifest['users'])} users  "
              f"({sum(1 for u in user_objs if u.role == 'student')} students, "
              f"{sum(1 for u in user_objs if u.role == 'company')} companies)")
        print(f"  {len(manifest['students'])} student profiles  "
              f"(active: {sum(1 for s in student_objs if s.account_status == 'active')}, "
              f"review: {sum(1 for s in student_objs if s.account_status == 'review')}, "
              f"deactivated: {sum(1 for s in student_objs if s.account_status == 'deactivated')})")
        print(f"  {len(manifest['companies'])} companies  "
              f"(approved: {sum(1 for c in company_objs if c.approval_status == 'approved')}, "
              f"pending: {sum(1 for c in company_objs if c.approval_status == 'pending')}, "
              f"rejected: {sum(1 for c in company_objs if c.approval_status == 'rejected')})")
        print(f"  {len(manifest['drives'])} drives  "
              f"(approved: {sum(1 for d in drive_objs if d.status == 'approved')}, "
              f"pending: {sum(1 for d in drive_objs if d.status == 'pending')}, "
              f"rejected: {sum(1 for d in drive_objs if d.status == 'rejected')}, "
              f"closed: {sum(1 for d in drive_objs if d.status == 'closed')})")
        print(f"  {len(manifest['applications'])} applications  "
              f"(applied: {sum(1 for a in application_objs if a.approval_status == 'applied')}, "
              f"shortlisted: {sum(1 for a in application_objs if a.approval_status == 'shortlisted')}, "
              f"selected: {sum(1 for a in application_objs if a.approval_status == 'selected')}, "
              f"rejected: {sum(1 for a in application_objs if a.approval_status == 'rejected')}, "
              f"hired: {sum(1 for a in application_objs if a.approval_status == 'hired')})")
        print(f"  Manifest saved to {SEED_MANIFEST}")
        print()
        print("  Notable test cases seeded:")
        print("  · Dan Rodrigues        — blacklisted student (User.status)")
        print("  · Isla Noronha         — deactivated student (Student.account_status)")
        print("  · Carol D'Souza        — student in review (cannot apply)")
        print("  · Seed RogueTech       — blacklisted company (User.status), drives closed")
        print("  · Seed DataInc         — rejected company")
        print("  · Seed BuildCo         — pending company")
        print("  · Frank / Grace        — 'hired' application status")
        print("  · Alice                — applied to 4 drives (all different, no duplicate)")


def destroy(app, db, User, Student, Company, Drive, Application):
    manifest = load_manifest()

    if not manifest:
        print("No seed manifest found. Nothing to destroy.")
        sys.exit(1)

    with app.app_context():
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

    from app import myApp
    from models import Application, Company, Drive, Student, User, db

    if args.create:
        create(myApp, db, User, Student, Company, Drive, Application)
    elif args.destroy:
        destroy(myApp, db, User, Student, Company, Drive, Application)