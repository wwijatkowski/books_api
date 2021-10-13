from app import db

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer)
    title = db.Column(db.String)
    authors = db.Column(db.String)
    published_date = db.Column(db.String)

    def __init__(self, book_id, title, authors, published_date):
        self.book_id = book_id
        self.title = title
        self.authors = authors
        self.published_date = published_date


db.create_all()
