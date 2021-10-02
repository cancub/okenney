from app import db as _db

class Consumption(_db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    category = _db.Column(_db.String(128), unique=False, nullable=False)
    product = _db.Column(_db.String(128), unique=False, nullable=False)
    unit = _db.Column(_db.String(128), unique=False, nullable=False)
    quantity = _db.Column(_db.Integer, unique=False, nullable=False)
    datetime = _db.Column(_db.DateTime, unique=False, nullable=False)

class Product(_db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String(128), unique=True, nullable=False)
    category = _db.Column(_db.String(128), unique=False, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

class Unit(_db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String(128), unique=False, nullable=False)
    category = _db.Column(_db.String(128), unique=False, nullable=False)

    def __repr__(self):
        return f'<Unit {self.name}>'

class Category(_db.Model):
    id = _db.Column(_db.Integer, primary_key=True)
    name = _db.Column(_db.String(128), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'