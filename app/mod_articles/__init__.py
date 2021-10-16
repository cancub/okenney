import os.path

from app.mod_articles.models import Article as _Article

IMAGES_PROJECT_PATH = 'static/images/articles'
ARTICLES_PROJECT_PATH = 'templates/articles'
ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
)
IMAGES_DIR = os.path.join(ROOT_DIR, IMAGES_PROJECT_PATH)
ARTICLES_DIR = os.path.join(ROOT_DIR, ARTICLES_PROJECT_PATH)

def get_latest_articles():
    latest_articles = []
    for a in _Article.query.order_by(_Article.dtime):
        latest_articles.append({'name': a.name, 'category': a.category})

    return latest_articles
