import flask
import flask_restful

from app.mod_articles import get_latest_articles

class ArticlesAPI(flask_restful.Resource):

    def get(self):
        return flask.jsonify(get_latest_articles(**flask.request.args))
