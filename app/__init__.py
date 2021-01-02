import json
from datetime import datetime
import os

# Import flask and template operators
import flask
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import DeclarativeMeta

# Define the WSGI application object
app = flask.Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported by modules and controllers.
db = SQLAlchemy(app)

# Define the API object.
api = Api(app)

class ConsumptionEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}

            for field in dir(obj):
                if (field.startswith('_')
                        or field.startswith('query')
                        or field == 'metadata'):
                    continue

                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                except TypeError:
                    try:
                        fields[field] = str(data)
                    except Exception:
                        fields[field] = None
                else:
                    fields[field] = data

            return fields

        return flask.json.JSONEncoder.default(self, obj)

app.json_encoder = ConsumptionEncoder

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True, nullable=False)
    filepath = db.Column(db.String(128), unique=True, nullable=False)
    dtime = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return f'<Article {self.title}>'

class Consumption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(128), unique=False, nullable=False)
    subtype = db.Column(db.String(128), unique=False, nullable=False)
    product = db.Column(db.String(128), unique=False, nullable=False)
    unit = db.Column(db.String(128), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    datetime = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return f'<Consumption {self.category}[{self.subtype}]>'

class ConsumptionAPI(Resource):
    def get(self):
        cat = flask.request.form['category']
        return flask.jsonify(
            {r.id: r for r in Consumption.query.filter_by(category=cat)},
        )

    def delete(self):
        cons_id = flask.request.form.get('id')
        cons = Consumption.query.filter_by(id=cons_id).first_or_404(
            description=f'Consumption {cons_id} does not exist.'
        )

        db.session.delete(cons)
        db.session.commit()

        return '', 204

    def put(self):
        try:
            dtime = datetime.strptime(
                flask.request.form['datetime'],
                '%Y-%m-%d %H:%M:%S.%f'
            )
        except KeyError:
            dtime = datetime.now()

        cons = Consumption(
            category = flask.request.form['category'],
            subtype = flask.request.form['subtype'],
            product = flask.request.form['product'],
            unit = flask.request.form['unit'],
            quantity = flask.request.form['quantity'],
            datetime = dtime
        )

        db.session.add(cons)
        db.session.commit()

        return flask.jsonify(cons)

api.add_resource(ConsumptionAPI, '/consumption_data')

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return flask.render_template('404.html'), 404

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

    return flask.render_template(
        'index.html',
        latest=latest_articles,
        total_count=len(latest_articles),
        preload_count=min(len(latest_articles), 5)
    )

# Everything else.
@app.route('/<path:subpath>')
def other(subpath):
    return flask.render_template(subpath)
