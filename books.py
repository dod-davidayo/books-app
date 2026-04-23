from flask import Flask, jsonify, request


app = Flask(__name__)


# using in memory
books = []
next_id = 1  # Auto-increment ID counter


# input validation
REQUIRED_FIELDS = ["title", "author", "isbn", "year"]

def validate_book(data, require_all=True):
    """
    Returns (cleaned_data, error_message).
    require_all=True, used for POST 
    require_all=False, used for PUT 
    """
    errors = []

    if require_all:
        for field in REQUIRED_FIELDS:
            if field not in data:
                errors.append(f"'{field}' is required.")

    # Validate types if fields are present
    if "title" in data and not isinstance(data["title"], str):
        errors.append("'title' must be a string.")

    if "author" in data and not isinstance(data["author"], str):
        errors.append("'author' must be a string.")

    if "isbn" in data and not isinstance(data["isbn"], str):
        errors.append("'isbn' must be a string.")

    if "year" in data:
        if not isinstance(data["year"], int) or data["year"] < 1000 or data["year"] > 2100:
            errors.append("'year' must be an integer between 1000 and 2100.")

    if errors:
        return None, errors

    return data, None

# to start the app
@app.route("/")
def home():
    return "Hello, Books App"


# read the all the books
@app.route("/books", methods=["GET"])
def get_books():
    return jsonify({
        "status": "success",
        "count": len(books),
        "books": books
    }), 200

# read one books
@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)

    if not book:
        return jsonify({"status": "error", "message": f"Book with id {book_id} not found."}), 404

    return jsonify({"status": "success", "book": book}), 200

# create a book
@app.route("/books", methods=["POST"])
def create_book():
    global next_id

    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Request body must be JSON."}), 400

    cleaned, errors = validate_book(data, require_all=True)
    if errors:
        return jsonify({"status": "error", "messages": errors}), 422

    new_book = {
        "id":     next_id,
        "title":  cleaned["title"],
        "author": cleaned["author"],
        "isbn":   cleaned["isbn"],
        "year":   cleaned["year"]
    }

    books.append(new_book)
    next_id += 1

    return jsonify({"status": "success", "book": new_book}), 201

# Update a book 
@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)

    if not book:
        return jsonify({"status": "error", "message": f"Book with id {book_id} not found."}), 404

    data = request.get_json()

    if not data:
        return jsonify({"status": "error", "message": "Request body must be JSON."}), 400

    cleaned, errors = validate_book(data, require_all=False)  # Partial update allowed
    if errors:
        return jsonify({"status": "error", "messages": errors}), 422

    # Only update fields that were provided
    for field in REQUIRED_FIELDS:
        if field in cleaned:
            book[field] = cleaned[field]

    return jsonify({"status": "success", "book": book}), 200

# Delete a book
@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global books

    book = next((b for b in books if b["id"] == book_id), None)

    if not book:
        return jsonify({"status": "error", "message": f"Book with id {book_id} not found."}), 404

    books = [b for b in books if b["id"] != book_id]

    return jsonify({"status": "success", "message": f"Book {book_id} deleted."}), 200

# to run the file
if __name__ == "__main__":
    app.run(debug=True)


# Global error handling
@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Route not found."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"status": "error", "message": "Method not allowed."}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"status": "error", "message": "Internal server error."}), 500
