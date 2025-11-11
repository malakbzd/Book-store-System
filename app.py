from flask import Flask

#  Importing all Blueprints
from users import users_bp
from books import books_bp
from sales import sales_bp
from reviews import reviews_bp
from statistics import statistics_bp

app = Flask(__name__)

#  Registering Blueprints
app.register_blueprint(users_bp, url_prefix="/users")
app.register_blueprint(books_bp, url_prefix="/books")
app.register_blueprint(sales_bp, url_prefix="/sales")
app.register_blueprint(reviews_bp, url_prefix="/reviews")
app.register_blueprint(statistics_bp, url_prefix="/stats")

# Home route (optional)
@app.route("/")
def home():
    return " Backend is Running!"

# Run Server
if __name__ == "__main__":
    app.run(debug=True)