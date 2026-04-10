# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# models/application.py
from datetime import datetime, timezone

from . import db


class Application(db.Model):
    __table_args__ = (
        db.UniqueConstraint("student_id", "drive_id"),
        db.CheckConstraint("rating >= 0 AND rating <= 5"),
    )
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False,
    )
    drive_id = db.Column(
        db.Integer,
        db.ForeignKey("drive.id"),
        nullable=False,
    )

    approval_status = db.Column(
        db.Enum("applied", "shortlisted", "selected", "rejected", "hired"), default="applied"
    )
    applied_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    feedBack = db.Column(db.Text, nullable=True, default="Not Provided")
    rating = db.Column(db.Integer, nullable=False,default=0)
    student = db.relationship("Student", back_populates="applications")
    drive = db.relationship("Drive", back_populates="applications")
