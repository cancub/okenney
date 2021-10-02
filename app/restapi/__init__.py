import flask
import flask_restful

Root = flask.Blueprint("RestRoot", __name__)

API = flask_restful.Api(Root)

from . import self_statistics as SelfStats
from app.mod_self_statistics import SELF_STATISTICS_PATH
API.add_resource(SelfStats.ConsumptionAPI, SELF_STATISTICS_PATH)
