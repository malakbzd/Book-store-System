from flask import Blueprint, request, jsonify
import sqlite3
import datetime

reviews_bp = Blueprint("reviews", __name__)

#  Database connection
def get_db():
    conn = sqlite3.connect("database/library.db")
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------------------------------
#  1. Add a Review to a Book
# ----------------------------------------------------
@reviews_bp.route("/add", methods=["POST"])
def add_review():
    data = request.get_json()

    user_id = data.get("user_id")
    book_id = data.get("book_id")
    rating = data.get("rating")
    comment = data.get("comment")

    #  Check required fields
    if not user_id or not book_id or rating is None:
        return jsonify({"error": "user_id, book_id, and rating are required"}), 400

    # Rating must be between 1 and 5
    if rating < 1 or rating > 5:
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    conn = get_db()

    #  Check if the book exists
    book = conn.execute("SELECT * FROM Books WHERE id = ?", (book_id,)).fetchone()
    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    #  Insert review
    conn.execute("""
        INSERT INTO Reviews (user_id, book_id, rating, comment, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, book_id, rating, comment, datetime.datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({"message": "Review added successfully ✅"})

# ----------------------------------------------------
#  2. Get All Reviews for a Specific Book
# ----------------------------------------------------
@reviews_bp.route("/book/<int:book_id>", methods=["GET"])
def get_reviews(book_id):
    conn = get_db()

    reviews = conn.execute("""
        SELECT Reviews.*, Users.name AS user_name
        FROM Reviews
        JOIN Users ON Users.id = Reviews.user_id
        WHERE book_id = ?
    """, (book_id,)).fetchall()

    conn.close()

    return jsonify([dict(row) for row in reviews])
