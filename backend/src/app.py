from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from db_models import db
from auth import auth_blueprint  # ✅ Импорт аутентификации
from tasks import tasks_blueprint  # ✅ Импорт маршрутов для задач
from users import users_blueprint  # ✅ Импорт маршрутов пользователей
from flask_cors import CORS  # ✅ Разрешение CORS
from flasgger import Swagger  # ✅ Импорт Swagger
from flasgger.utils import swag_from

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# ✅ Разрешаем CORS для всех маршрутов
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# ✅ Настройка Swagger UI с поддержкой авторизации через Bearer Token
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Task Manager API",
        "description": "API documentation for Task Manager",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your Bearer token in the format: Bearer <TOKEN>"
        }
    },
    "security": [{"Bearer": []}]
}

swagger = Swagger(app, template=swagger_template)

# ✅ Регистрируем маршруты
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(tasks_blueprint, url_prefix="/tasks")
app.register_blueprint(users_blueprint, url_prefix="/users")


@app.route("/", methods=["GET"])
@swag_from({
    "tags": ["System"],
    "summary": "API Health Check",
    "description": "Returns a simple JSON message indicating that the API is running.",
    "responses": {
        200: {
            "description": "API is up and running",
            "schema": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "example": "API is running!"
                    }
                }
            }
        }
    }
})
def home():
    """Health check endpoint"""
    return jsonify({"message": "API is running!"}), 200


# ✅ Глобальная обработка preflight-запросов (CORS)
@app.before_request
def handle_options():
    """Разрешает preflight OPTIONS-запросы перед отправкой запросов с токеном"""
    if request.method == "OPTIONS":
        response = jsonify({"message": "Preflight OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
        return response, 200


# ✅ Создаём таблицы, если их нет
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
