import os.path
import re

import flask

from app.mod_articles.models import Article as _Article

INTERNAL_PATH = '/articles'

PROJECT_IMAGES_PATH = 'static/images/articles'
PROJECT_ARTICLES_PATH = 'templates/articles'

REQUEST_IMAGES_PATH = PROJECT_IMAGES_PATH
REQUEST_ARTICLES_PATH = 'articles'

ROOT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
)
LOCAL_IMAGES_DIR = os.path.join(ROOT_DIR, PROJECT_IMAGES_PATH)
LOCAL_ARTICLES_DIR = os.path.join(ROOT_DIR, PROJECT_ARTICLES_PATH)

def article_images_dir_path(category, filename, remote=True):
    base_path = os.path.join(category, filename)
    if remote:
        root_path = REQUEST_IMAGES_PATH
    else:
        root_path = LOCAL_IMAGES_DIR

    return os.path.join(root_path, base_path)

def article_category_path(category, remote=True):
    if remote:
        root_path = REQUEST_ARTICLES_PATH
    else:
        root_path = LOCAL_ARTICLES_DIR

    return os.path.join(root_path, category)

def get_contents(path):
    # Get the contents of the file.
    with open(path, 'r') as F:
        contents = F.read()

    # Retrieve the title and description, using what we know about how the
    # file must be structured.
    p = re.compile(
        r'{%\s*macro titre\(\)\s*%}\s*([^{]*)\s*{%\s*endmacro\s*%}'
    )
    title = p.search(contents).groups(0)[0]

    p = re.compile(
        r'{%\s*macro description\(\)\s*%}\s*([^{]*)\s*{%\s*endmacro\s*%}'
    )
    description = p.search(contents).groups(0)[0]

    return title, description

def get_latest_articles(
    category=None,
    end_datetime=None,
    batch_size=None,
    provide_title = True,
    provide_description = True,
    provide_article_path = True,
    provide_image_path = True,
    remote_request = True,
):
    article_query = _Article.query

    if category is not None:
        article_query = article_query.filter_by(category=category)
    if end_datetime is not None:
        article_query = article_query.filter(_Article.dtime < end_datetime)

    # Make sure we present the articles in reverse chronological order (i.e.,
    # newest to oldest).
    article_query = article_query.order_by(_Article.dtime.desc())

    if batch_size is not None:
        # Only return the number of desired articles.
        article_query = article_query.limit(int(batch_size))

    articles = article_query.all()

    # Add in whatever additional information the caller needs.
    # NOTE:
    # Our JSONEncoder just looks at dir(item) for DeclarativeMeta objects when
    # building a dict, so we're safe to just add attributes to these objects
    # and have them processed by our encoder.
    for article in articles:
        name = article.name

        # Collect the root that we will use for internal referencing (e.g., to
        # get the full title).
        local_article_root = os.path.join(
            article_category_path(article.category, remote=False),
            name,
        )

        if provide_title or provide_description:
            # Reach into the file and collect the title and description via the
            # magic of regex. Avoid multiple loads of the file into memory by
            # collecting both even if we only need one.
            title, description = get_contents(local_article_root + '.html')

            if provide_title:
                article.title = title
            if provide_description:
                article.description = description

        if provide_article_path:
            remote_article_path = article_category_path(
                article.category,
                remote=remote_request,
            )
            article.filepath = f'{remote_article_path}/{name}.html'

        if provide_image_path:
            article.image_dir = article_images_dir_path(
                article.category,
                name,
                remote=remote_request,
            )

    return articles
