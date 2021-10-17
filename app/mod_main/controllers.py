import os
import flask

from . import ARTICLE_CATEGORIES, ARTICLE_BATCH_COUNT, ARTICLE_PRELOAD_COUNT
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
        'preload_count': min(article_count, ARTICLE_PRELOAD_COUNT),
        'batch_size': ARTICLE_BATCH_COUNT,
        'article_api_url': flask.url_for('RestRoot.articles'),
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

    if subpath != 'index.html':
        # We're rendeing a specific article, so we need to let it know where it
        # can find its images.
        base_name = os.path.splitext(subpath)[0]
        context['image_dir'] = (
            f'/{_articles.PROJECT_IMAGES_PATH}/{category}/{base_name}'
        )

    return flask.render_template(f'/articles/{category}/{subpath}', **context)
