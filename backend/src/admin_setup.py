from db_models import db, User
from werkzeug.security import generate_password_hash
from app import app  # ✅ Подключаем Flask-приложение

# ✅ Создаём контекст приложения для работы с базой данных
with app.app_context():
    # Проверяем, есть ли уже админ
    if not User.query.filter_by(username="admin").first():
        admin = User(
            username="admin",
            email="admin@example.com",
            password_hash=generate_password_hash("admin"),
            role="admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Админ создан: логин 'admin', пароль 'admin'")
    else:
        print("⚠️ Админ уже существует!")
