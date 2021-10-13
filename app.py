from flask import Flask, render_template, request, json
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

import models


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/books-list')
def books_list():
    # Cleaning data base for model Book before new request
    db.session.query(models.Book).delete()
    db.session.commit()

    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit')
    if response.status_code == 200:
        books_founded = response.json()
        books = books_founded['items']
        for item in books:
            book = models.Book(item['id'],
                               item['volumeInfo']['title'],
                               item['volumeInfo']['authors'][0],
                               item['volumeInfo']['publishedDate']
                               )
            db.session.add(book)
            db.session.commit()
        all = db.session.query(models.Book).all()

        return render_template('bookslist.html', all=all)


@app.route('/book-list-sort')
def sort_data():

    choice = request.args.get('sort_type')
    if choice == 'ascending':
        all = db.session.query(models.Book).order_by(models.Book.published_date)
    else:
        choice == 'descending'
        all = db.session.query(models.Book).order_by(-models.Book.published_date)

    return render_template('bookslist.html', all=all)


@app.route('/filter-by-title')
def filter_data():

    data = request.args.get('data')
    filtered_data = db.session.query(models.Book).filter_by(title=data).all()

    return render_template('bookslist.html', all=filtered_data)


@app.route('/filter-by-authors')
def filter_authors():

    data = request.args.get('data')
    filtered_data = db.session.query(models.Book).filter_by(authors=data).all()

    return render_template('bookslist.html', all=filtered_data)


@app.route('/filter-by-published_date')
def filter_published_date():

    data = request.args.get('data')
    filtered_data = db.session.query(models.Book).filter_by(published_date=data).all()

    return render_template('bookslist.html', all=filtered_data)


@app.route('/book-details')
def book_details():
    book_id = request.args.get('book_id')

    response = requests.get(f'https://www.googleapis.com/books/v1/volumes/{book_id}')

    if response.status_code == 200:
        book = response.json()

        # This handling an exception is because sometimes there is no imageLinks - not exist
        try:
            thumbnail = book['volumeInfo']['imageLinks']['thumbnail']
        except KeyError:
            thumbnail = ''

        return render_template('bookdetails.html', book=book, thumbnail=thumbnail)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
