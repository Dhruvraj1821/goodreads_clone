from flask_login import UserMixin
from app import db  # ✅ Import the existing db from __init__.py

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    books = db.relationship('UserBook', back_populates='user')

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ol_id = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    year = db.Column(db.String(10))
    users = db.relationship('UserBook', back_populates='book')

class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    review = db.Column(db.Text)
    rating = db.Column(db.Integer)

    user = db.relationship('User', back_populates='books')
    book = db.relationship('Book', back_populates='users')
