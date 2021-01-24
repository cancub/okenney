import json
from datetime import datetime as _datetime
from datetime import date as _date
from datetime import timedelta as _timedelta
import os

# Import flask and template operators
import flask
from flask_login import LoginManager
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

# Define the login manager.
# login_manager = LoginManager()
# login_manager.init_app(app)

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
    product = db.Column(db.String(128), unique=False, nullable=False)
    unit = db.Column(db.String(128), unique=False, nullable=False)
    quantity = db.Column(db.Integer, unique=False, nullable=False)
    datetime = db.Column(db.DateTime, unique=False, nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    category = db.Column(db.String(128), unique=False, nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

class Unit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    category = db.Column(db.String(128), unique=False, nullable=False)

    def __repr__(self):
        return f'<Unit {self.name}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __repr__(self):
        return f'<Category {self.name}>'

class ConsumptionAPI(Resource):
    default_quantity_units = {
        'cigarettes': None,
        'alcohol': 'ml'
    }

    def _consom_par_id(self, cons_id):
        return Consumption.query.filter_by(id=cons_id).first_or_404(
            description=f'Consumption {cons_id} does not exist.'
        )

    def _product_query(self, cat_name, product_name):
        return Product.query.filter_by(category=cat_name, name=product_name)

    def _check_and_add_product(self, cat_name, product_name):
        # Add a new product if this is the first time we're seeing it.
        prod = None
        if self._product_query(cat_name, product_name).count() == 0:
            prod = Product(category=cat_name, name=product_name)
            db.session.add(prod)
        return prod

    def _check_and_clear_products(self, cat_name):
        # Look though all the Products to see if any Consumptions exist with
        # that product. If not, get rid of it.
        del_ids = []
        for p in Product.query.filter_by(category=cat_name):
            if Consumption.query.filter_by(product=p.name).count() == 0:
                del_ids.append(p.id)
                db.session.delete(p)
        return del_ids

    def _strptime(self, datetime_string):
        formats = [
            '%Y-%m-%dT%H:%M:%S.000Z',
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%d %H:%M',
            '%Y-%m-%d',
        ]
        for f in formats:
            try:
                return _datetime.strptime(datetime_string, f)
            except ValueError:
                pass
        raise ValueError

    def get(self):
        try:
            cat = flask.request.args['category']
        except KeyError:
            return flask.jsonify(Consumption.query.all())

        # Determine how the data should be collected.
        x_unit = flask.request.args.get('x_unit', 'days')
        if x_unit not in ('days', 'weeks', 'months'):
            abort(400, msg=f'Unrecognized time unit {x_unit}')

        # Determine what quantity unit the front-end is expecting. If none is
        # specified
        y_unit = flask.request.args.get(
            'y_unit',
            self.default_quantity_units[cat]
        )

        data = {}

        # Get the set of data corresponding to this category and collect it
        # based on the unit of time.
        # TODO: allow for time units other than days.
        now = _datetime.now().date()
        first_date = now
        for r in Consumption.query.filter_by(category=cat):
            date = r.datetime.date()

            # Is this the earliest date?
            if date < first_date:
                first_date = date

            # TODO: format the quantity to match what was requested as the
            #       y_unit.

            # Add the data to the output.
            try:
                data[str(date)] += float(r.quantity)
            except KeyError:
                data[str(date)] = float(r.quantity)

        # Add today if it is missing.
        if now not in data:
            data[str(now)] = 0

        # Make sure there are at least 10 days represented.
        if first_date > now - _timedelta(days=10):
            first_date = now - _timedelta(days=10)
            data[str(first_date)] = 0

        # Fill in the other dates between the first date and today.
        for days in range((now - first_date).days):
            candidate_date = str(now - _timedelta(days=days))
            if candidate_date not in data:
                data[candidate_date] = 0

        # Our D3 functions require iterables.
        return flask.jsonify(
            [{'date': k, 'value': v} for k,v in data.items()]
        )

    def delete(self):
        db.session.delete(
            self._consom_par_id(flask.request.form.get('id'))
        )

        # We also want to check if this was the only Consumption of this
        # product, in which case we remove it from our products table/
        del_product_ids = self._check_and_clear_products(
            flask.request.form['category']
        )

        db.session.commit()

        return flask.jsonify({'del_product_ids': del_product_ids})

    def put(self):
        cons = self._consom_par_id(flask.request.form.get('id'))

        cat_name = flask.request.form['category']
        product_name = flask.request.form['product']

        for key, val in flask.request.form.items():
            if key == 'id':
                continue
            if key == 'datetime':
                val = self._strptime(val)

            setattr(cons, key, val)

        # We may have switched to a brand new product.
        new_product = self._check_and_add_product(cat_name, product_name)

        # Or maybe this modification removed the only consumption that was
        # using this product, in which case we want to get rid of it.
        del_product_ids = self._check_and_clear_products(cat_name)

        db.session.commit()

        return flask.jsonify({
            'consom': cons,
            'new_product': new_product,
            'del_product_ids': del_product_ids,
        })

    def post(self):
        try:
            dtime = flask.request.form['datetime']
        except KeyError:
            dtime = _datetime.now()
        else:
            if dtime.strip() == '':
                dtime = _datetime.now()
            else:
                try:
                    dtime = self._strptime(dtime)
                except ValueError:
                    dtime = _datetime.now()

        cat_name = flask.request.form['category']
        product_name = flask.request.form['product']

        cons = Consumption(
            category = cat_name,
            product = product_name,
            unit = flask.request.form['unit'],
            quantity = flask.request.form['quantity'],
            datetime = dtime
        )
        db.session.add(cons)

        # Add a new product if this is the first time we're seeing it.
        new_product = self._check_and_add_product(cat_name, product_name)

        db.session.commit()

        # Make sure to include the ID
        return flask.jsonify({
            'consom': cons,
            'new_product': new_product,
        })

CONSUMPTION_PATH = '/consumption-data'
api.add_resource(ConsumptionAPI, CONSUMPTION_PATH)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return flask.render_template('404.html'), 404

@app.route('/')
def index():
    latest_articles = []
    for a in Article.query.order_by(Article.dtime):
        image_path = 'static/images/{}'.format(
            a.filepath.split('articles/')[-1].replace('.html', '.png')
        )

        desc_path = a.filepath.replace('.html', '-desc.html')

        latest_articles.append({
            'title': a.title.title().replace('Test', 'TEST'),
            'filepath': a.filepath,
            'image': image_path,
            'desc': desc_path,
        })


    context = {
        'latest': latest_articles,
        'total_count': len(latest_articles),
        'preload_count': min(len(latest_articles), 5),
        'CONSUMPTION_API': CONSUMPTION_PATH
    }

    return flask.render_template('index.html', **context)

@app.route('/about/')
@app.route('/about/<path:subpath>')
def about(subpath=None):
    if subpath is None:
        subpath = 'index.html'

    return flask.render_template(
        f'about/{subpath}',
        CONSUMPTION_API= CONSUMPTION_PATH
    )

@app.route('/ideas/')
@app.route('/ideas/<path:subpath>')
def ideas(subpath=None):
    if subpath is None:
        subpath = 'index.html'
    return flask.render_template(f'ideas/{subpath}')

@app.route('/philosophy/')
@app.route('/philosophy/<path:subpath>')
def philosophy(subpath=None):
    if subpath is None:
        subpath = 'index.html'
    return flask.render_template(f'philosophy/{subpath}')

@app.route('/politics/')
@app.route('/politics/<path:subpath>')
def politics(subpath=None):
    if subpath is None:
        subpath = 'index.html'
    return flask.render_template(f'politics/{subpath}')

@app.route('/projects/')
@app.route('/projects/<path:subpath>')
def projects(subpath=None):
    if subpath is None:
        subpath = 'index.html'
    return flask.render_template(f'projects/{subpath}')

@app.route('/control')
def control():
    return flask.render_template(
        'control.html',
        categories = Category.query.all(),
        products = Product.query.all(),
        units = Unit.query.all(),
        CONSUMPTION_API = CONSUMPTION_PATH
    )

@app.route('/chart')
def chart():
    return flask.render_template(
        'chart.html',
        CONSUMPTION_API= CONSUMPTION_PATH
    )

# Everything else.
@app.route('/<path:subpath>')
def other(subpath):
    return flask.render_template(subpath)
