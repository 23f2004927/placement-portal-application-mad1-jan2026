# Christiano Blairoy Fernandes
# 23f2004927
# 6 April 2026
# seed.py

from werkzeug.security import generate_password_hash

from app import myApp
from models import User, db

with myApp.app_context():
    # 1. Create the physical tables based on your models
    db.create_all()

    # 2. Check if admin exists to avoid duplicates
    if User.query.filter_by(username="admin").first() is None:
        admin = User(
            username="admin",
            email="admin@portal.com",
            role="admin",
            password_hash=generate_password_hash("admin123"),
        )

        # 3. The "Handshake"
        db.session.add(admin)  # Stage the change
        db.session.commit()  # Save to the .db file
        print("Admin user created successfully!")
    else:
        print("Admin already exists. Skipping...")
