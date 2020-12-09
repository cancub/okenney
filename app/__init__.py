# Import flask and template operators
from flask import Flask, render_template
from flask_restful import Resource, Api

from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
api = Api(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    filepath = db.Column(db.String(128), unique=True, nullable=False)
    dtime = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return '<Article %r>' % self.title

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def index():
    return render_template(
        Article.query.order_by(Article.dtime).first().filepath
    )
