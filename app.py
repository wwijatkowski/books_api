from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import requests

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
    response = requests.get('https://www.googleapis.com/books/v1/volumes?q=Hobbit')

    if response.status_code == 200:
        books_founded = response.json()
        books = books_founded['items']

        return render_template('bookslist.html', books=books)




if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
