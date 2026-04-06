# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# models/drive.py

from datetime import datetime, timezone

from . import db


class Drive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company.id"),
        nullable=False,
    )
    job_title = db.Column(
        db.String(100),
        nullable=False,
    )
    job_description = db.Column(db.Text, nullable=False)
    job_type = db.Column(db.Text, nullable=False, default="Intership")
    eligibility_criteria = db.Column(db.Text)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.Enum("pending", "approved", "rejected", "blacklisted"), default="pending"
    )
    ctc = db.Column(db.Text, nullable=False, default="Performance Based")
    location = db.Column(db.Text, nullable=False, default="Remote")
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    application_deadline = db.Column(db.DateTime, nullable=False)

    company = db.relationship("Company", back_populates="drives")
    applications = db.relationship("Application", back_populates="drive")
