from app import db as _db

class Article(_db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    title = _db.Column(_db.String(128), unique=True, nullable=False)
    filepath = _db.Column(_db.String(128), unique=True, nullable=False)
    dtime = _db.Column(_db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return f'<Article {self.title}>'
