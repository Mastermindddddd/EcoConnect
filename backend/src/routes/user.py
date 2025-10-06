from flask import Blueprint, jsonify, request

# Create the Blueprint
user_bp = Blueprint("user", __name__)

# Example route: GET /api/users
@user_bp.route("/users", methods=["GET"])
def get_users():
    # Dummy user list (replace with database queries later)
    users = [
        {"id": 1, "name": "Alice"},
        {"id": 2, "name": "Bob"},
        {"id": 3, "name": "Charlie"},
    ]
    return jsonify(users)

# Example route: POST /api/users
@user_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    new_user = {
        "id": 999,  # placeholder; later you’ll generate IDs from DB
        "name": data["name"]
    }
    return jsonify(new_user), 201
