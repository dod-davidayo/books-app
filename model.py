from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Author table (One author to many books)
class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    books = db.relationship('Book', backref='author', lazy=True)

#Category table
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(50), nullable=False)

# Book table
class Book(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    isbn = db.Column(db.String(20))
    year = db.Column(db.Integer)

    # Foreign Keys
    author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    Category_id = db.Column(db.Integer, db.ForeignKey('category.id'))