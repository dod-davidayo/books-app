from flask import Flask, jsonify, request
from flask_migrate import Migrate
from model import db, Book, Author, Category
from db_config import Config


# books.py is the app.py
app = Flask(__name__)
app.config.from_object(Config)

# Config must come before init_app, otherwise it will not work
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   

db.init_app(app)
migrate = Migrate(app, db)

# Create the database tables
with app.app_context():
    db.create_all()



@app.route("/")
def index():
    return (" welcome to books API")

# Get /books with pagination, search fitering
@app.route('/books', methods=['GET'])
def get_books():
    query = Book.query

    # Search by title
    title = request.args.get('title')
    if title:
        query = query.filter(Book.title.contains(title))

    #  Filter by year 
    year = request.args.get('year')
    if year:
        query = query.filter_by(year=year)

    # Pagination
    page = int(request.args.get('page', 1, ))
    Limit = int(request.args.get('limit',5,))

    books =query.paginate(page=page, per_page=Limit)

    result = []

    for book in books.items:
        result.append({
            "id": book.id,
            "title": book.title,
            "author": book.author.name if book.author else None,
            "year": book.year,
        })

    return jsonify({
        "total": books.total,
        "pages": books.pages,
        "data": result
    })

#POST  /books
@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    # create or get author

    author = Author.query.filter_by(name=data["author"].first()).first()
    if not author:
        author = Author(name=data["author"])
        db.session.add(author)
        
# Create book
    book = Book(
        title=data["title"],
        isbn=data.get("isbn"),
        year=data.get("year"),
        author=author
    )


    db.session.add(book)
    db.session.commit()
    return jsonify({"message": "Book created"}), 201

# PUT /books/<id>
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    book = Book.query.get_or_404(id)
    
    if not book:
        return jsonify({"message": "Book not found"}), 404

    data = request.get_json()

    book.title = data.get("title", book.title)
    book.year = data.get("year", book.year)


    db.session.commit()
    return jsonify({"message": "Book updated"})

# Delete /books/<id>
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get_or_404(id)

    if not book:
        return jsonify({"message": "Book not found"}), 404

    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted"})



#  ERROR HANDLERS
@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "message": "Route not found."}), 404

@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({"status": "error", "message": "Method not allowed."}), 405

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"status": "error", "message": "Internal server error."}), 500


if __name__ == "__main__":
    app.run(debug=True)