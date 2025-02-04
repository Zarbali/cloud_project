from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), default="user")  # ✅ Добавляем роль пользователя

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """Хешируем пароль перед сохранением"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Проверяем пароль"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username} - {self.role}>"


class Task(db.Model):
    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="To Do", nullable=False)  # ✅ Добавляем статус задачи
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # ✅ user_id может быть NULL для общего доступа
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", backref="tasks")

    def __repr__(self):
        return f"<Task {self.title} - {self.status} by user {self.user_id}>"
