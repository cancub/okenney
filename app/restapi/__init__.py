import functools

import flask
import flask_login
import flask_restful

Root = flask.Blueprint('RestRoot', __name__)

API = flask_restful.Api(Root)

def admin_access_only(view):
    """
    Decorator to validate a session:
      - User is logged in.
      - Session is not timed out.
    """
    @functools.wraps(view)
    @flask_login.login_required
    def wrapped_view(*args, **kwargs):
        if flask_login.current_user.name != 'admin':
            flask.abort(401)
        return view(*args, **kwargs)
    return wrapped_view

from . import self_statistics as SelfStats
from app.mod_self_statistics import SELF_STATISTICS_PATH
API.add_resource(
    SelfStats.ConsumptionAPI,
    SELF_STATISTICS_PATH,
    endpoint='self_stats',
)

from . import articles as Articles
from app.mod_articles import INTERNAL_PATH as ARTICLES_PATH
API.add_resource(
    Articles.ArticlesAPI,
    ARTICLES_PATH,
    endpoint='articles'
)
