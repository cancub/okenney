import json
from datetime import datetime as _datetime
from datetime import date as _date
from datetime import timedelta as _timedelta
import os
import re

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
        if flask.request.args.get('raw'):
            return flask.jsonify(Consumption.query.all())

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

_default_quantity_units = {
    'beer': 'mL',
    'wine': 'mL',
    'spirit': 'fl oz',
    'cannabis': 'toke',
    'chips': 'g',
    'cigarette': 'cigarette',
    'coffee': 'mL',
}

def _translate_quantity(consom):
    # Figure out what unit we'd like the output to be in.
    target_unit = _default_quantity_units[consom.category]

    if consom.unit.startswith(target_unit):
        return consom.quantity

    target_unit_quant = float(
        re.search(rf'\(([\d\.]+) {target_unit}\)', consom.unit).group(1)
    )
    return target_unit_quant * float(consom.quantity)

def get_chart_data():
    '''
    Build a day-by-day breakdown of consumption for each category.
    '''
    categories = [c.name for c in Category.query.all()]
    data = {c: {} for c in categories}

    # Keep track of the earliest date we've seen.
    now = _datetime.now().date()
    min_date = now

    # Also keep track of the maximum value we've seen for each category.
    maximums = {c: 0.1 for c in categories}

    # Collect all of the data
    for c in Consumption.query.all():
        category = c.category
        date = c.datetime.date()
        quantity = _translate_quantity(c)

        min_date = min(min_date, date)

        try:
            data[category][str(date)] += quantity
        except KeyError:
            data[category][str(date)] = quantity

        maximums[category] = max(maximums[category], data[category][str(date)])

    # Now walk through the data and fill in the blanks with zeros.
    dates = [
        str(min_date + _timedelta(days=d))
            for d in range((now-min_date).days + 1)
    ]
    for date in dates:
        for cat, cat_data in data.items():
            if str(date) not in cat_data:
                cat_data[str(date)] = 0

    # Finally, reformat the data so that it is a list of dicts.
    data_list = []
    for cat, cat_data in data.items():
        for date, value in cat_data.items():
            data_list.append({'category': cat, 'date': date, 'value': value})

    return {
        'data': data_list,
        'categories': categories,
        'dates': dates,
        'maximums': maximums,
        'units': _default_quantity_units,
    }

def get_latest_articles():
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

    return latest_articles

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return flask.render_template('404.html'), 404

@app.route('/')
def index():

    latest_articles = get_latest_articles()
    article_count = len(latest_articles)

    context = {
        'latest': latest_articles,
        'total_count': article_count,
        'preload_count': min(article_count, 5),
        'consumption_data': get_chart_data(),
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

# Everything else.
@app.route('/<path:subpath>')
def other(subpath):
    return flask.render_template(subpath)
