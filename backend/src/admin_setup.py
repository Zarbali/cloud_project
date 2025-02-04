from db_models import db, User
from werkzeug.security import generate_password_hash
from app import app


with app.app_context():

    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=generate_password_hash("admin"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created: login 'admin', password 'admin'")
    else:
        print("⚠️ The admin already exists!")
