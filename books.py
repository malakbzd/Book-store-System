from flask import Blueprint, request, jsonify
import sqlite3

# Books Blueprint
books_bp = Blueprint("books", __name__)

#  Database connection
def get_db():
    conn = sqlite3.connect("database/library.db")
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------------------------------
# Get all books
# ----------------------------------------------------
@books_bp.route("/all", methods=["GET"])
def get_all_books():
    conn = get_db()
    books = conn.execute("SELECT * FROM Books").fetchall()
    conn.close()
    return jsonify([dict(row) for row in books])

# ----------------------------------------------------
#  Get a single book by ID
# ----------------------------------------------------
@books_bp.route("/<int:book_id>", methods=["GET"])
def get_book(book_id):
    conn = get_db()
    book = conn.execute("SELECT * FROM Books WHERE id = ?", (book_id,)).fetchone()
    conn.close()

    if book:
        return jsonify(dict(book))
    return jsonify({"error": "Book not found"}), 404

# ----------------------------------------------------
# Add a new book (Admin only)
# ----------------------------------------------------
@books_bp.route("/add", methods=["POST"])
def add_book():
    data = request.get_json()

    #  Check admin role
    if data.get("role") != "admin":
        return jsonify({"error": "Only admin can add books"}), 403

    title = data.get("title")
    author = data.get("author")
    publisher = data.get("publisher")
    publish_year = data.get("publish_year")
    price = data.get("price")
    stock = data.get("stock")
    description = data.get("description")

    if not title:
        return jsonify({"error": "Book title is required"}), 400

    conn = get_db()
    conn.execute(
        """
        INSERT INTO Books (title, author, publisher, publish_year, price, stock, description)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (title, author, publisher, publish_year, price, stock, description),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Book added successfully"})

# ----------------------------------------------------
# Update book (Admin only)
# ----------------------------------------------------
@books_bp.route("/update/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.get_json()

    # Check admin role
    if data.get("role") != "admin":
        return jsonify({"error": "Only admin can update books"}), 403

    conn = get_db()
    book = conn.execute("SELECT * FROM Books WHERE id = ?", (book_id,)).fetchone()

    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    conn.execute(
        """
        UPDATE Books 
        SET title=?, author=?, publisher=?, publish_year=?, price=?, stock=?, description=?
        WHERE id=?
        """,
        (
            data.get("title", book["title"]),
            data.get("author", book["author"]),
            data.get("publisher", book["publisher"]),
            data.get("publish_year", book["publish_year"]),
            data.get("price", book["price"]),
            data.get("stock", book["stock"]),
            data.get("description", book["description"]),
            book_id,
        ),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Book updated successfully"})

# ----------------------------------------------------
#  Delete book (Admin only)
# ----------------------------------------------------
@books_bp.route("/delete/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    data = request.get_json()

    # Check admin role
    if data.get("role") != "admin":
        return jsonify({"error": "Only admin can delete books"}), 403

    conn = get_db()
    book = conn.execute("SELECT * FROM Books WHERE id = ?", (book_id,)).fetchone()

    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    conn.execute("DELETE FROM Books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Book deleted successfully"})
