from flask import Blueprint, request, jsonify
from db_models import db, Task, User
from auth import token_required
from flask_cors import CORS, cross_origin
from flasgger import swag_from
from flask import jsonify
import redis



tasks_blueprint = Blueprint("tasks", __name__)
CORS(tasks_blueprint, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)

# ✅ Retrieving all tasks (user sees only his own, admin - all)
@tasks_blueprint.route("/", methods=["GET"])
@token_required
@cross_origin()
@swag_from({
      "tags": ["Tasks"],
    "summary": "Get all tasks for the logged-in user (Admin sees all, with caching)",
    "responses": {
        200: {"description": "List of tasks"},
        401: {"description": "Unauthorized"}
    }
})
def get_tasks(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Ключ для кеша в зависимости от пользователя
    cache_key = f"tasks_user_{user_id}" if user.role != "admin" else "tasks_admin"

    # ✅ Проверяем, есть ли кешированные данные
    cached_tasks = redis_client.get(cache_key)
    if cached_tasks:
        print(f"✅ Данные загружены из Redis: {cache_key}")  # Логируем
        return jsonify({"tasks": eval(cached_tasks)}), 200  # Если есть, возвращаем кеш

    # ❌ Кеш отсутствует, загружаем из БД
    tasks = Task.query.all() if user.role == "admin" else Task.query.filter_by(user_id=user_id).all()
    tasks_data = [{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat(),
    } for task in tasks]

    # ✅ Записываем данные в Redis (на 60 сек)
    redis_client.setex(cache_key, 60, str(tasks_data))
    print(f"✅ Данные кешированы в Redis: {cache_key}")

    return jsonify({"tasks": tasks_data}), 200

# ✅ Retrieve tasks for a specific user (for admins only)You've hit your limit. Please try again later.
@tasks_blueprint.route("/admin/<int:target_user_id>", methods=["GET"])
@token_required
@cross_origin()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Get tasks for a specific user (Admin only)",
    "parameters": [
        {
            "name": "target_user_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the user whose tasks should be retrieved"
        }
    ],
    "responses": {
        200: {"description": "List of tasks for the given user"},
        403: {"description": "Forbidden"},
        404: {"description": "User not found"}
    }
})
def get_user_tasks(user_id, target_user_id):
    admin = User.query.get(user_id)
    if not admin or admin.role != "admin":
        return jsonify({"error": "Insufficient permissions"}), 403

    user = User.query.get(target_user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    tasks = Task.query.filter_by(user_id=target_user_id).all()

    return jsonify([{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat(),
    } for task in tasks]), 200


# ✅ Create a new task

@tasks_blueprint.route("/", methods=["POST"])
@token_required
@cross_origin()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Create a new task",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "example": "My Task"},
                    "description": {"type": "string", "example": "This is a test task"},
                    "status": {"type": "string", "enum": ["To Do", "In Progress", "Done"], "example": "To Do"}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Task created successfully"},
        400: {"description": "Missing required fields"},
        401: {"description": "Unauthorized"}
    }
})
def create_task(user_id):
    data = request.json
    title = data.get("title")
    description = data.get("description", "")
    status = data.get("status", "To Do")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_task = Task(title=title, description=description, status=status, user_id=user_id)
    db.session.add(new_task)
    db.session.commit()
    redis_client.delete("tasks_admin")
    redis_client.delete(f"tasks_user_{user_id}")

    return jsonify({
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "user_id": new_task.user_id,
        "created_at": new_task.created_at.isoformat(),
    }), 201


# ✅ Task update
@tasks_blueprint.route("/<int:task_id>", methods=["PUT"])
@token_required
@cross_origin()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Update a task",
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the task to update"
        },
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "example": "Updated Task"},
                    "description": {"type": "string", "example": "Updated task description"},
                    "status": {"type": "string", "enum": ["To Do", "In Progress", "Done"], "example": "Done"}
                }
            }
        }
    ],
    "responses": {
        200: {"description": "Task updated successfully"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Task not found"}
    }
})
def update_task(user_id, task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    if task.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    data = request.json
    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)

    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "user_id": task.user_id,
        "created_at": task.created_at.isoformat(),
    }), 200


# ✅ Deleting tasks (user can delete only his own tasks, admin can delete any tasks)
@tasks_blueprint.route("/<int:task_id>", methods=["DELETE"])
@token_required
@cross_origin()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Delete a task",
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the task to delete"
        }
    ],
    "responses": {
        200: {"description": "Task successfully deleted"},
        401: {"description": "Unauthorized"},
        403: {"description": "Forbidden"},
        404: {"description": "Task not found"}
    }
})
def delete_task(user_id, task_id):
    user = User.query.get(user_id)
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"error": "Task not found"}), 404
    if user.role != "admin" and task.user_id != user_id:
        return jsonify({"error": "Forbidden"}), 403

    db.session.delete(task)
    db.session.commit()
    redis_client.delete("tasks_admin")
    redis_client.delete(f"tasks_user_{task.user_id}")

    return jsonify({"message": "Task successfully deleted"}), 200

# ✅ Deleting a task by admin (separate route)

@tasks_blueprint.route("/admin/delete/<int:task_id>", methods=["DELETE"])
@token_required
@cross_origin()
@swag_from({
    "tags": ["Tasks"],
    "summary": "Delete any task as an admin",
    "parameters": [
        {
            "name": "task_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of the task to delete"
        }
    ],
    "responses": {
        200: {"description": "Task successfully deleted by admin"},
        403: {"description": "Forbidden"},
        404: {"description": "Task not found"}
    }
})
def admin_delete_task(user_id, task_id):
    """Function for deleting a task by the administrator."""
    admin = User.query.get(user_id)
    if not admin or admin.role != "admin":
        return jsonify({"error": "Insufficient permissions"}), 403

    task = Task.query.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task successfully deleted by admin"}), 200

@tasks_blueprint.route("/tasks/cache", methods=["GET"])
@token_required
@cross_origin()
def get_tasks_with_cache(user_id):
    """Cache check: retrieve tasks from Redis (if any)"""
    cache_key = f"tasks_user_{user_id}" if user_id != "admin" else "tasks_admin"

    cached_tasks = redis_client.get(cache_key)
    if cached_tasks:
        return jsonify({"tasks": eval(cached_tasks)}), 200  # Преобразуем строку обратно в список

    return jsonify({"message": "Cache is empty"}), 200

# ✅ Global processing of preflight requests (CORS)
@tasks_blueprint.before_request
def handle_options():
    """Globally allow OPTIONS requests for preflight CORS"""
    if request.method == "OPTIONS":
        response = jsonify({"message": "Preflight OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
        return response, 200
