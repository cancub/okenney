import os

# Import flask and template operators
from flask import Flask, render_template, url_for

from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

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
    latest_articles = []
    for a in Article.query.order_by(Article.dtime):
        image_path = 'static/images/{}'.format(
            a.filepath.split('articles/')[-1].replace('.html','.png')
        )

        desc_path = a.filepath.replace('.html', '-desc.html')

        latest_articles.append({
            'title': a.title.title().replace('Test', 'TEST'),
            'filepath': a.filepath,
            'image': image_path,
            'desc': desc_path,
        })

    return render_template(
        'index.html',
        latest=latest_articles,
        total_count=len(latest_articles),
        preload_count=min(len(latest_articles), 5)
    )
