# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# models/__init__.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .application import Application
from .company import Company
from .drive import Drive
from .student import Student
from .user import User
