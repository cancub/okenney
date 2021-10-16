import os
import flask

from . import ARTICLE_CATEGORIES
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

@mod_main.route('/articles/<category>/')
@mod_main.route('/articles/<category>/<path:subpath>')
def other(category, subpath='index.html'):
    if category not in ARTICLE_CATEGORIES:
        return flask.render_template('404.html'), 404

    context = {}

    if category == 'about' and subpath in ('index.html', 'vices.html'):
        context.update({
            'consumption_data': _self_stats.get_chart_data(),
            'CONSUMPTION_API': '/api' + _self_stats.SELF_STATISTICS_PATH,
        })


    return flask.render_template(f'/articles/{category}/{subpath}', **context)
