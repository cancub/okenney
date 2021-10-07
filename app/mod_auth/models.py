import flask_login
from app import db as _db

class User(flask_login.UserMixin, _db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    email = _db.Column(_db.String(100), unique=True)
    password = _db.Column(_db.String(100))
    name = _db.Column(_db.String(1000), unique=True)

    def __repr__(self):
        return '<User %r>' % self.name
