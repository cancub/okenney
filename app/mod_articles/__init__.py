import datetime
import html.parser as HTMLParser
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

class HTMLWordCounter(HTMLParser.HTMLParser):
    def __init__(self):
        super(HTMLWordCounter, self).__init__()
        self.word_count = 0
    def handle_data(self, data):
        if self.get_starttag_text() != 'script':
            self.word_count += len(data.split())

class LocaleContents(object):
    def __init__(self, full_contents, locale='en'):
        self._contents = full_contents
        self._locale = locale
        self.title = None
        self.description = None
        self.text = None
        self.word_count = None

        self._process_file()

    def _collect_string(self, type, name):
        if self._locale  == 'en':
            locale_name = name
        else:
            locale_name = f'{name}_{self._locale}'

        p = re.compile(
            fr'{type}\s+{locale_name}\s*%}}\s*([\W\w\s]*?)\s*{{%\s*end{type}'
        )

        try:
            return p.search(self._contents).groups(0)[0]
        except AttributeError:
            return ''

    def _collect_macro_contents(self, name):
        return self._collect_string('macro', name + '\(\)')

    def _collect_block_contents(self, name):
        return self._collect_string('block', name)

    def _process_file(self):
        self.title = self._collect_macro_contents('titre')
        self.description = self._collect_macro_contents('description')
        self.text = self._collect_block_contents('article_texte')

        counter = HTMLWordCounter()
        counter.feed(self.text)
        self.word_count = counter.word_count

class ArticleDetails(object):
    def __init__(self, article_path):
        self.path = article_path

        with open(article_path, 'r') as F:
            self.contents = F.read()

        self.fr = LocaleContents(self.contents, 'fr')
        self.en = LocaleContents(self.contents, 'en')

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

def get_articles(
    category=None,
    end_datetime=None,
    batch_size=None,
    provide_title=True,
    provide_description=True,
    provide_article_path=True,
    provide_image_path=True,
    process_datetime=True,
    remote_request=True,
    reverse_order=False,
):
    article_query = _Article.query

    if category is not None:
        article_query = article_query.filter_by(category=category)
    if end_datetime is not None:
        article_query = article_query.filter(_Article.dtime < end_datetime)
    if reverse_order:
        # Make sure we present the articles in reverse chronological order
        # (i.e., newest to oldest).
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
            contents = ArticleDetails(f'{local_article_root}.html')

            if provide_title:
                article.title = contents.en.title
            if provide_description:
                article.description = contents.en.description

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


def get_latest_articles(**kwargs):
    return get_articles(reverse_order=True, **kwargs)