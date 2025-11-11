from flask import Blueprint, request, jsonify
import sqlite3
import datetime

#  Users Blueprint
users_bp = Blueprint("users", __name__)

#  Database connection
def get_db():
    conn = sqlite3.connect("database/library.db")
    conn.row_factory = sqlite3.Row
    return conn

# ---------------------------------------------------------
#  Register a New User
# ---------------------------------------------------------
@users_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Check if all fields are provided
    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db()

    try:
        conn.execute("""
            INSERT INTO Users (name, email, password, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (name, email, password, "user", datetime.datetime.utcnow().isoformat()))

        conn.commit()

    except sqlite3.IntegrityError:
        # Email already exists in database
        return jsonify({"error": "Email already in use"}), 400

    finally:
        conn.close()

    return jsonify({"message": "User registered successfully "})

# ---------------------------------------------------------
# Login
# ---------------------------------------------------------
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = get_db()
    user = conn.execute("SELECT * FROM Users WHERE email = ?", (email,)).fetchone()
    conn.close()

    # User not found
    if not user:
        return jsonify({"error": "Account not found"}), 400

    # Password check (simple version — no hashing)
    if password != user["password"]:
        return jsonify({"error": "Incorrect password"}), 400

    # Successful login
    return jsonify({
        "message": "Login successful ",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"],
            "created_at": user["created_at"]
        }
    })
