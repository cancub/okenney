import flask
import flask_login

import app.mod_self_statistics.models as _models
from app.mod_self_statistics import SELF_STATISTICS_PATH

mod_self_stats = flask.Blueprint(
    'self_stats',
    __name__,
    url_prefix='/self_stats'
)

@mod_self_stats.route('/control')
@mod_self_stats.route('/control/<path:subpath>')
@flask_login.login_required
def control(subpath=None):
    template_fname = 'control'

    if subpath == 'detailed':
        template_fname += '-detailed'

    return flask.render_template(
        template_fname + '.html',
        categories=_models.Category.query.all(),
        products=_models.Product.query.all(),
        units=_models.Unit.query.all(),
        CONSUMPTION_API='/api' + SELF_STATISTICS_PATH,
        SIMPLE_CONTROL_URL=flask.url_for('self_stats.control'),
        DETAILED_CONTROL_URL=flask.url_for('self_stats.control') + '/detailed',
    )
