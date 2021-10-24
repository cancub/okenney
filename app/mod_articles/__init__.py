import datetime
import os.path
import re

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

def process_file_contents(path):
    result = {'fr': {}, 'en': {}}

    # Get the contents of the file.
    with open(path, 'r') as F:
        contents = F.read()

    def collect_string(template_type, name):
        p = re.compile(
            f'{{%\\s*{template_type}\\s+{name}\\s*%}}'
            + '\\s*([^{{]*)\\s*'
            + f'{{%\\s*end{template_type}\\s*%}}'
        )

        try:
            return p.search(contents).groups(0)[0]
        except AttributeError:
            return ''

    def collect_macro_contents(name):
        return collect_string('macro', name + '\\(\\)')

    def collect_block_contents(name):
        return collect_string('block', name)

    # Retrieve the titles.
    result['fr']['title'] = collect_macro_contents('titre_fr')
    result['en']['title'] = collect_macro_contents('titre')

    # Repeat with descriptions.
    result['fr']['description'] = collect_macro_contents('description_fr')
    result['en']['description'] = collect_macro_contents('description')

    # And finally with the text itself.
    result['fr']['text'] = collect_block_contents('article_texte_fr')
    result['en']['text'] = collect_block_contents('article_texte')

    return result

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

def datetime_to_relative_string(dtime):
    '''
    Take a datetime object and covert it to a string relative to the current
    date. That is, if the datetime is from today, report just the time,
    otherwise report just the date.
    '''
    # If the article was published today, specify the time, otherwise use
    # the date.
    if datetime.datetime.now().date() == dtime.date():
        formatter = '%H:%M'
    else:
        formatter = '%B %d, %Y'

    return datetime.datetime.strftime(dtime, formatter)

def get_article(subpath, process_datetime=True):
    article = _Article.query.filter_by(name=subpath).one()

    if process_datetime:
        article.date_str = datetime_to_relative_string(article.dtime)

    return article

def get_latest_articles(
    category=None,
    end_datetime=None,
    batch_size=None,
    provide_title=True,
    provide_description=True,
    provide_article_path=True,
    provide_image_path=True,
    process_datetime=True,
    remote_request=True,
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
            contents = process_file_contents(local_article_root + '.html')

            if provide_title:
                article.title = contents['en']['title']
            if provide_description:
                article.description = contents['en']['description']

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

        if process_datetime:
            article.date_str = datetime_to_relative_string(article.dtime)

    return articles
