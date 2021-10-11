from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.String)
    title = db.Column(db.String)
    authors = db.Column(db.String)
    published_date = db.Column(db.String)
    categories = db.column(db.String)
    average_rating = db.Column(db.Integer)
    ratings_count = db.Column(db.Integer)
    thumbnail = db.Column(db.String)

    def __init__(self, book_id, title, authors, published_date, categories, average_rating, ratings_count, thumbnail):
        self.book_id = book_id
        self.title = title
        self.authors = authors
        self.published_date = published_date
        self.categories = categories
        self.average_rating = average_rating
        self.ratings_count = ratings_count
        self.thumbnail = thumbnail


db.create_all()
