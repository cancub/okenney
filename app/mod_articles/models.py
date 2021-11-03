from app import db as _db

class Article(_db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String(128), unique=True, nullable=False)
    # name_fr = _db.Column(_db.String(128), unique=True, nullable=False)
    category = _db.Column(_db.String(128), unique=False, nullable=False)
    dtime = _db.Column(_db.DateTime, unique=False, nullable=False)
    # last_updated = _db.Column(_db.DateTime, unique=False, nullable=False)
    word_count = _db.Column(_db.Integer, unique=False, nullable=False)
    # word_count_fr = _db.Column(_db.Integer, unique=False, nullable=False)
    # view_count = _db.Column(_db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f'<Article {self.name}>'
