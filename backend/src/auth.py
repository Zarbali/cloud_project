from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db_models import db, User
import jwt
import datetime
from functools import wraps
from config import Config
from flasgger import swag_from
from flask_cors import CORS, cross_origin

auth_blueprint = Blueprint("auth", __name__)
CORS(auth_blueprint, resources={r"/*": {"origins": "*"}}, supports_credentials=True)



def generate_token(user_id):

    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)  # Истекает через 12 часов
    }
    token = jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")
    return token



def decode_token(token):

    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None



def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token is missing or invalid"}), 401

        token = token.split(" ")[1]  # Убираем "Bearer "
        user_id = decode_token(token)
        if not user_id:
            return jsonify({"error": "Invalid or expired token"}), 401

        return f(user_id, *args, **kwargs)

    return decorated_function


# ✅ Проверка роли (админ)
def is_admin(user_id):

    user = User.query.get(user_id)
    return user and user.role == "admin"



@auth_blueprint.route("/register", methods=["POST"])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)  # ✅ Разрешаем CORS
@swag_from({
    "tags": ["Auth"],
    "summary": "Register a new user",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "example": "newuser"},
                    "email": {"type": "string", "example": "newuser@example.com"},
                    "password": {"type": "string", "example": "mypassword"},
                },
            },
        }
    ],
    "responses": {
        "201": {"description": "User successfully registered"},
        "400": {"description": "Bad request (Missing fields or user already exists)"},
    },
})
def register():

    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password_hash=hashed_password, role="user")
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


# ✅ Логин пользователя
@auth_blueprint.route("/login", methods=["POST"])
@cross_origin(origins="http://localhost:3000", supports_credentials=True)
@swag_from({
    "tags": ["Auth"],
    "summary": "User login",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "username": {"type": "string", "example": "admin"},
                    "password": {"type": "string", "example": "admin"},
                },
            },
        }
    ],
    "responses": {
        "200": {"description": "Successful login"},
        "401": {"description": "Unauthorized - Invalid credentials"},
    },
})
def login():

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username or password"}), 401

    token = generate_token(user.id)
    return jsonify({"token": token, "role": user.role}), 200



@auth_blueprint.route("/check_role", methods=["GET"])
@token_required
@cross_origin(origins="http://localhost:3000", supports_credentials=True)  # ✅ Разрешаем CORS
@swag_from({
    "tags": ["Auth"],
    "responses": {
        "200": {"description": "Returns user role"},
        "401": {"description": "Unauthorized - Invalid or expired token"},
    },
})
def check_role(user_id):

    user = User.query.get(user_id)
    if user:
        return jsonify({"role": user.role}), 200
    return jsonify({"role": "user"}), 200


# ✅ Получение данных текущего пользователя
@auth_blueprint.route("/me", methods=["GET", "OPTIONS"])
@token_required
@cross_origin(origins="http://localhost:3000", supports_credentials=True)  # ✅ Разрешаем CORS
def get_me(user_id):

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200



@auth_blueprint.before_request
def handle_options():
    """Разрешает preflight OPTIONS-запросы"""
    if request.method == "OPTIONS":
        response = jsonify({"message": "Preflight OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
        return response, 200
