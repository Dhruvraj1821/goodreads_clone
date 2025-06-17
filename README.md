# Goodreads Clone

This is a basic Goodreads clone built using Flask. The application allows users to register, log in, search for books using the Open Library API, add them to a personal bookshelf, and leave reviews and ratings.

## Features

- User registration and authentication
- Book search functionality using the Open Library API
- Users can add books to their personal bookshelf
- Users can leave star ratings and written reviews
- View all reviews left by users on a book
- Responsive HTML templates for each feature

## Technologies Used

- Python (Flask)
- Flask SQLAlchemy
- Flask Login
- MySQL (via mysql-connector)
- HTML (Jinja templating)
- Open Library API

## Project Structure
goodreads_clone/
│
├── app/
│ ├── templates/
│ │ ├── base.html
│ │ ├── home.html
│ │ ├── login.html
│ │ ├── register.html
│ │ ├── search.html
│ │ ├── bookshelf.html
│ │ ├── book_detail.html
│ │ └── reviews.html
│ ├── init.py
│ ├── forms.py
│ ├── models.py
│ └── routes.py
│
├── config.py
├── run.py
└── venv/


## Setup Instructions

1. **Clone the repository**
2. **Create a virtual environment**
3. **Install the dependencies**
for manual installation : pip install flask flask-login flask-sqlalchemy mysql-connector-python requests
4. **Update the database URI in `config.py`**
Make sure the `SQLALCHEMY_DATABASE_URI` matches your MySQL setup.
5. **Create the database and tables**
from app import db, create_app
app = create_app()
with app.app_context():
... db.create_all()
6. **Run the application**
Visit the site in your browser at `http://localhost:5000`.



