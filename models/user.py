# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# models/user.py

from datetime import datetime, timezone

from . import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(256))
    role = db.Column(db.Enum("admin", "student", "company"))
    is_active = db.Column(db.Boolean, default=True)
    is_blacklisted = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    company = db.relationship("Company", back_populates="user")
    student = db.relationship("Student", back_populates="user")
