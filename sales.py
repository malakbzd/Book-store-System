from flask import Blueprint, request, jsonify
import sqlite3
import datetime

sales_bp = Blueprint("sales", __name__)

#  Database connection
def get_db():
    conn = sqlite3.connect("database/library.db")
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------------------------------
#  1. Buy a Book
# ----------------------------------------------------
@sales_bp.route("/buy", methods=["POST"])
def buy_book():
    data = request.get_json()

    user_id = data.get("user_id")
    book_id = data.get("book_id")
    quantity = data.get("quantity")

    # Validate required data
    if not user_id or not book_id or not quantity:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db()

    # Get book info
    book = conn.execute("SELECT * FROM Books WHERE id = ?", (book_id,)).fetchone()

    if not book:
        conn.close()
        return jsonify({"error": "Book not found"}), 404

    #  Check stock availability
    if book["stock"] < quantity:
        conn.close()
        return jsonify({"error": "Not enough stock available"}), 400

    #  Calculate total price
    total_price = book["price"] * quantity

    #  Update stock
    conn.execute("UPDATE Books SET stock = stock - ? WHERE id = ?", (quantity, book_id))

    #  Insert sale record
    conn.execute("""
        INSERT INTO Sales (user_id, book_id, quantity, total_price, sale_date)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, book_id, quantity, total_price, datetime.datetime.utcnow().isoformat()))

    conn.commit()
    conn.close()

    return jsonify({"message": "Purchase completed successfully ", "total_price": total_price})

# ----------------------------------------------------
#  2. Get a User's Purchases
# ----------------------------------------------------
@sales_bp.route("/my/<int:user_id>", methods=["GET"])
def my_sales(user_id):
    conn = get_db()
    sales = conn.execute("""
        SELECT Sales.*, Books.title
        FROM Sales
        JOIN Books ON Books.id = Sales.book_id
        WHERE Sales.user_id = ?
    """, (user_id,)).fetchall()
    conn.close()

    return jsonify([dict(row) for row in sales])

# ----------------------------------------------------
#  3. Get All Sales (Admin Only)
# ----------------------------------------------------
@sales_bp.route("/all", methods=["GET"])
def all_sales():
    conn = get_db()
    sales = conn.execute("""
        SELECT Sales.*, Users.name AS buyer, Books.title AS book_title
        FROM Sales
        JOIN Users ON Users.id = Sales.user_id
        JOIN Books ON Books.id = Sales.book_id
    """).fetchall()
    conn.close()

    return jsonify([dict(row) for row in sales])
