import datetime
import flask
import flask_restful

from app import db as _db
from app.mod_self_statistics import models as _models


class ConsumptionAPI(flask_restful.Resource):

    def _consom_par_id(self, cons_id):
        return _models.Consumption.query.filter_by(id=cons_id).first_or_404(
            description=f'Consumption {cons_id} does not exist.'
        )

    def _product_query(self, cat_name, product_name):
        return _models.Product.query.filter_by(
            category=cat_name,
            name=product_name,
        )

    def _check_and_add_product(self, cat_name, product_name):
        # Add a new product if this is the first time we're seeing it.
        prod = None
        if self._product_query(cat_name, product_name).count() == 0:
            prod = _models.Product(category=cat_name, name=product_name)
            _db.session.add(prod)
        return prod

    def _check_and_clear_products(self, cat_name):
        # Look though all the Products to see if any Consumptions exist with
        # that product. If not, get rid of it.
        del_ids = []
        for p in _models.Product.query.filter_by(category=cat_name):
            items = _models.Consumption.query.filter_by(product=p.name)
            if items.count() == 0:
                del_ids.append(p.id)
                _db.session.delete(p)
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
                return datetime.datetime.strptime(datetime_string, f)
            except ValueError:
                pass
        raise ValueError

    def get(self):
        if flask.request.args.get('raw'):
            return flask.jsonify(_models.Consumption.query.all())

    def delete(self):
        _db.session.delete(
            self._consom_par_id(flask.request.form.get('id'))
        )

        # We also want to check if this was the only Consumption of this
        # product, in which case we remove it from our products table/
        del_product_ids = self._check_and_clear_products(
            flask.request.form['category']
        )

        _db.session.commit()

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

        _db.session.commit()

        return flask.jsonify({
            'consom': cons,
            'new_product': new_product,
            'del_product_ids': del_product_ids,
        })

    def post(self):
        try:
            dtime = flask.request.form['datetime']
        except KeyError:
            dtime = datetime.datetime.now()
        else:
            if dtime.strip() == '':
                dtime = datetime.datetime.now()
            else:
                try:
                    dtime = self._strptime(dtime)
                except ValueError:
                    dtime = datetime.datetime.now()

        cat_name = flask.request.form['category']
        product_name = flask.request.form['product']

        cons = _models.Consumption(
            category=cat_name,
            product=product_name,
            unit=flask.request.form['unit'],
            quantity=flask.request.form['quantity'],
            datetime=dtime
        )
        _db.session.add(cons)

        # Add a new product if this is the first time we're seeing it.
        new_product = self._check_and_add_product(cat_name, product_name)

        _db.session.commit()

        # Make sure to include the ID
        return flask.jsonify({
            'consom': cons,
            'new_product': new_product,
        })
