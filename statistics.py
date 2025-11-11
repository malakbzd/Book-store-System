from flask import Blueprint, jsonify
import sqlite3

statistics_bp = Blueprint("statistics", __name__)

# Database connection
def get_db():
    conn = sqlite3.connect("database/library.db")
    conn.row_factory = sqlite3.Row
    return conn

# ----------------------------------------------------
#  1. Top Selling Books
# ----------------------------------------------------
@statistics_bp.route("/top-selling", methods=["GET"])
def top_selling():
    conn = get_db()

    result = conn.execute("""
        SELECT Books.id, Books.title, Books.author,
               IFNULL(SUM(Sales.quantity), 0) AS total_sales
        FROM Books
        LEFT JOIN Sales ON Books.id = Sales.book_id
        GROUP BY Books.id
        ORDER BY total_sales DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in result])

# ----------------------------------------------------
#  2. Top Rated Books
# ----------------------------------------------------
@statistics_bp.route("/top-rated", methods=["GET"])
def top_rated():
    conn = get_db()

    result = conn.execute("""
        SELECT Books.id, Books.title, Books.author,
               IFNULL(AVG(Reviews.rating), 0) AS average_rating
        FROM Books
        LEFT JOIN Reviews ON Books.id = Reviews.book_id
        GROUP BY Books.id
        ORDER BY average_rating DESC
        LIMIT 10
    """).fetchall()

    conn.close()

    return jsonify([dict(row) for row in result])
