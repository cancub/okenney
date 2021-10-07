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
@flask_login.login_required
def control():
    return flask.render_template(
        'control.html',
        categories=_models.Category.query.all(),
        products=_models.Product.query.all(),
        units=_models.Unit.query.all(),
        CONSUMPTION_API='/api' + SELF_STATISTICS_PATH
    )
