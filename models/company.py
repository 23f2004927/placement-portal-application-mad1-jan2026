# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# models/company.py

from datetime import datetime, timezone

from . import db


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True
    )
    company_name = db.Column(db.String(100), nullable=False, unique=True)
    hr_contact = db.Column(db.String(100))
    website = db.Column(db.String(200))
    description = db.Column(db.Text)
    approval_status = db.Column(
        db.Enum("pending", "approved", "rejected", "blacklisted"), default="pending"
    )
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship("User", back_populates="company")
    drives = db.relationship("Drive", back_populates="company")
