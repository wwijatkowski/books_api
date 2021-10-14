import os

from flask import Flask, render_template, request, json, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests
from sqlalchemy.exc import InterfaceError

from forms import SearchField

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Data_base.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'sweihfjnwejhgdfkefdhw;lw;w;w'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

import models


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    """
    This searching data from API on site https://www.googleapis.com/books/v1/volumes
    and show an screen results into table.
    """

    form = SearchField()

    def data_converter(data):
        """
        Because data is type -> list.
        Function check if data is in corrent format (str) for save into data base. If not, convert into str.
        :param data: one item from json file
        :return: str
        """
        output_string = ''
        for i in data:
            output_string += i
        return output_string

    if request.method == 'POST':
        # Cleaning data base for model Book before new request
        db.session.query(models.Book).delete()
        db.session.commit()

        title = form.title.data
        params = {"q": title}
        response = requests.get('https://www.googleapis.com/books/v1/volumes', params=params)
        if response.status_code == 200:
            data_response = response.json()
            books = data_response['items']
            for item in books:
                ### It is neede to oparate this instance because not always is all data to create object to data base.
                try:
                    book = models.Book(item['id'],
                                       item['volumeInfo']['title'],
                                       data_converter(item['volumeInfo']['authors']),
                                       item['volumeInfo']['publishedDate']
                                       )
                    db.session.add(book)
                    db.session.commit()
                except KeyError:
                    pass
            return redirect(url_for('books_list'))
        else:
            flash('Nothing found. try again')
            return redirect(url_for('search'))

    return render_template('search.html', form=form)

@app.route('/books-list/')
def books_list():
    """
    Take data from data base about books were taken from API nad show into tabel.
    """

    all = db.session.query(models.Book).all()
    return render_template('bookslist.html', all=all)


@app.route('/book-list-sort')
def sort_data():
    """
    Take data from data base about books were taken from API, sort ascending or descending and finally show into tabel.
    """
    choice = request.args.get('sort_type')
    if choice == 'ascending':
        all = db.session.query(models.Book).order_by(models.Book.published_date)
    else:
        choice == 'descending'
        all = db.session.query(models.Book).order_by(-models.Book.published_date)

    return render_template('bookslist.html', all=all)


@app.route('/filter-by-title')
def filter_title():
    """
    Filter data by title which was chosen.
    """
    data = request.args.get('data')
    filtered_data = db.session.query(models.Book).filter_by(title=data).all()

    return render_template('bookslist.html', all=filtered_data)


@app.route('/filter-by-authors')
def filter_authors():
    """
    Filter data by authors which was chosen.
    """
    data = request.args.get('data')
    filtered_data = db.session.query(models.Book).filter_by(authors=data).all()

    return render_template('bookslist.html', all=filtered_data)


@app.route('/filter-by-published_date')
def filter_published_date():
    """
    Filter data by published_date which was chosen.
    """
    data = request.args.get('data')
    filtered_data = db.session.query(models.Book).filter_by(published_date=data).all()

    return render_template('bookslist.html', all=filtered_data)


@app.route('/book-details')
def book_details():
    """
    Show details of chosen book.
    """
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
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
