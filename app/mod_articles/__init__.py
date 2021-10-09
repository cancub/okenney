import os.path

from app.mod_articles.models import Article as _Article

def get_latest_articles():
    latest_articles = []
    for a in _Article.query.order_by(_Article.dtime):
        # Obtain the image and description paths from the name of the article.
        image_root = 'static/images/{}'.format(
            os.path.splitext(a.filepath.split('articles/')[-1])[0]
        )
        desc_path = a.filepath.replace('.html', '-desc.html')

        # TODO:
        # Get rid of the "TEST" modification once we have actual articles.
        latest_articles.append({
            'title': a.title.title().replace('Test', 'TEST'),
            'filepath': a.filepath,
            'image': image_root,
            'desc': desc_path,
        })

    return latest_articles
