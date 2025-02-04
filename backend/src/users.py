from flask import Blueprint, jsonify, request
from db_models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from auth import token_required
from flask_cors import CORS
from flasgger import swag_from

users_blueprint = Blueprint("users", __name__)
CORS(users_blueprint, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# ✅ Getting the list of users (Only for admins)
@users_blueprint.route("/", methods=["GET"])
@token_required
@swag_from({
    "tags": ["Users"],
    "summary": "Get list of all users (admin only)",
    "responses": {
        200: {
            "description": "List of users",
            "schema": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "example": 1},
                        "username": {"type": "string", "example": "user123"},
                        "email": {"type": "string", "example": "user@example.com"},
                        "role": {"type": "string", "example": "admin"}
                    }
                }
            }
        },
        403: {"description": "Insufficient permissions"}
    }
})
def get_users(user_id):
    user = User.query.get(user_id)
    if not user or user.role != "admin":
        return jsonify({"error": "Insufficient permissions"}), 403

    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "email": u.email, "role": u.role}
        for u in users
    ]), 200


# ✅ Getting information about the current user
@users_blueprint.route("/me", methods=["GET"])
@token_required
@swag_from({
    "tags": ["Users"],
    "summary": "Get current logged-in user information",
    "responses": {
        200: {"description": "Returns user details"},
        404: {"description": "User not found"}
    }
})
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


# ✅ Getting information about a user by ID (for admins)
@users_blueprint.route("/<int:user_id>", methods=["GET"])
@token_required
@swag_from({
    "tags": ["Users"],
    "summary": "Get user details by ID (admin only)",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "User ID"
        }
    ],
    "responses": {
        200: {"description": "User details retrieved successfully"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "User not found"}
    }
})
def get_user_by_id(admin_id, user_id):
    """Allows the administrator to retrieve user information by user ID"""
    admin = User.query.get(admin_id)
    if not admin or admin.role != "admin":
        return jsonify({"error": "Insufficient permissions"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }), 200


# ✅ Deleting an account by a user

@users_blueprint.route("/delete", methods=["DELETE"])
@token_required
@swag_from({
    "tags": ["Users"],
    "summary": "Delete your own account",
    "responses": {
        200: {"description": "Account deleted successfully"},
        404: {"description": "User not found"}
    }
})
def delete_self(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "Account deleted successfully"}), 200


# ✅ Deleting a user by admin

@users_blueprint.route("/admin/delete/<int:user_id>", methods=["DELETE"])
@token_required
@swag_from({
    "tags": ["Users"],
    "summary": "Delete a user (admin only)",
    "parameters": [
        {
            "name": "user_id",
            "in": "path",
            "type": "integer",
            "required": True,
            "description": "ID of user to delete"
        }
    ],
    "responses": {
        200: {"description": "User successfully deleted"},
        403: {"description": "Insufficient permissions"},
        404: {"description": "User not found"}
    }
})
def delete_user(admin_id, user_id):
    admin = User.query.get(admin_id)
    if not admin or admin.role != "admin":
        return jsonify({"error": "Insufficient permissions"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": "User successfully deleted"}), 200


# ✅ Global preflight request processing (CORS)

@users_blueprint.before_request
def handle_options():
    """Enables preflight OPTIONS requests"""
    if request.method == "OPTIONS":
        response = jsonify({"message": "Preflight OK"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
        return response, 200
