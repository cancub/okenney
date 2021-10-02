import flask

import app.mod_articles as _articles
import app.mod_self_statistics as _self_stats

mod_main = flask.Blueprint('main', __name__)

@mod_main.route('/')
def index():
    latest_articles = _articles.get_latest_articles()
    article_count = len(latest_articles)

    context = {
        'latest': latest_articles,
        'total_count': article_count,
        'preload_count': min(article_count, 5),
        'consumption_data': _self_stats.get_chart_data(),
    }

    return flask.render_template('index.html', **context)

@mod_main.route('/about/')
@mod_main.route('/about/<path:subpath>')
def about(subpath=None):
    context = {
        'CONSUMPTION_API': '/api' + _self_stats.SELF_STATISTICS_PATH,
    }

    if subpath is None:
        subpath = 'index.html'
    elif subpath == 'vices.html':
        context['consumption_data'] = _self_stats.get_chart_data()

    return flask.render_template(f'about/{subpath}', **context)

@mod_main.route('/ideas/')
@mod_main.route('/ideas/<path:subpath>')
def ideas(subpath=None):
    if subpath is None:
        subpath = 'index.html'
    return flask.render_template(f'ideas/{subpath}')

@mod_main.route('/philosophy/')
@mod_main.route('/philosophy/<path:subpath>')
def philosophy(subpath=None):
    if subpath is None:
        subpath = 'index.html'
    return flask.render_template(f'philosophy/{subpath}')

@mod_main.route('/politics/')
@mod_main.route('/politics/<path:subpath>')
def politics(subpath=None):
    if subpath is None:
        subpath = 'index.html'
    return flask.render_template(f'politics/{subpath}')

@mod_main.route('/projects/')
@mod_main.route('/projects/<path:subpath>')
def projects(subpath=None):
    if subpath is None:
        subpath = 'index.html'
    return flask.render_template(f'projects/{subpath}')

# Everything else.
@mod_main.route('/<path:subpath>')
def other(subpath):
    return flask.render_template(subpath)

# Errors.
@mod_main.errorhandler(404)
def not_found(error):
    return flask.render_template('404.html'), 404
