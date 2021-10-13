from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests
from jinja2 import UndefinedError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/Data_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/books-list')
def books_list():
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit', )

    if response.status_code == 200:
        books_founded = response.json()
        books = books_founded['items']

        return render_template('bookslist.html', books=books)


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
