from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/Data_base.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/books-list'):
def books_list():



if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
