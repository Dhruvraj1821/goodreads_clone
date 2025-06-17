from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import RegisterForm, LoginForm
from app.models import User, Book, UserBook, db
import requests

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('home.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Try logging in.', 'danger')
            return redirect(url_for('main.login'))

        hashed_password = generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash('Registration successful! Welcome!', 'success')
        return redirect(url_for('main.home'))
    return render_template('register.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.home'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.home'))

@main.route('/search')
def search():
    query = request.args.get('q')
    books = []
    if query:
        response = requests.get(f"https://openlibrary.org/search.json?q={query}")
        if response.status_code == 200:
            data = response.json()
            books = data['docs'][:10]
    return render_template('search.html', books=books)

@main.route('/add_to_bookshelf', methods=['POST'])
@login_required
def add_to_bookshelf():
    ol_id = request.form['ol_id']
    title = request.form['title']
    author = request.form['author']
    year = request.form['year']

    book = Book.query.filter_by(ol_id=ol_id).first()
    if not book:
        book = Book(ol_id=ol_id, title=title, author=author, year=year)
        db.session.add(book)
        db.session.commit()

    if not UserBook.query.filter_by(user_id=current_user.id, book_id=book.id).first():
        user_book = UserBook(user_id=current_user.id, book_id=book.id)
        db.session.add(user_book)
        db.session.commit()
        flash('Book added to your shelf!', 'success')
    else:
        flash('Book already in your shelf.', 'info')

    return redirect(url_for('main.bookshelf'))

@main.route('/bookshelf')
@login_required
def bookshelf():
    bookshelf = UserBook.query.filter_by(user_id=current_user.id).all()
    return render_template('bookshelf.html', bookshelf=bookshelf)

@main.route('/review/<int:userbook_id>', methods=['POST'])
@login_required
def review_book(userbook_id):
    entry = UserBook.query.get_or_404(userbook_id)
    if entry.user_id != current_user.id:
        flash("Unauthorized to review this book.", 'danger')
        return redirect(url_for('main.bookshelf'))

    entry.review = request.form.get('review')
    entry.rating = int(request.form.get('rating'))
    db.session.commit()
    flash('Review submitted!', 'success')
    return redirect(url_for('main.bookshelf'))

@main.route('/reviews/<int:book_id>')
def public_reviews(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = UserBook.query.filter_by(book_id=book_id).filter(UserBook.review.isnot(None)).all()
    return render_template('reviews.html', book=book, reviews=reviews)

@main.route('/book/<int:book_id>')
def book_detail(book_id):
    book = Book.query.get_or_404(book_id)
    reviews = UserBook.query.filter_by(book_id=book_id).filter(UserBook.review != None).all()
    return render_template('book_detail.html', book=book, reviews=reviews)
