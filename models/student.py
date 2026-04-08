# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# models/student.py

from datetime import datetime, timezone

from . import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True
    )
    full_name = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    graduation_year = db.Column(db.Integer)
    cgpa = db.Column(db.Float)
    skills = db.Column(db.Text)
    gender = db.Column(
        db.Enum("Male", "Female", "Other", "Prefer Not To Say"),
        nullable=False,
        default="Prefer Not To Say",
    )
    socials = db.Column(db.JSON, nullable=True)
    account_status = db.Column(
        db.Enum("review", "active", "deactivated", "blacklisted"), default="active"
    )
    resume_filename = db.Column(db.String(200))
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="student")
    applications = db.relationship("Application", back_populates="student")
