import json

import flask
import flask_login
import flask_sqlalchemy
from sqlalchemy.ext.declarative import DeclarativeMeta
from werkzeug.routing import Rule


# Define the WSGI application object
app = flask.Flask(__name__)

# Configurations.
app.config.from_object('config')

# Define the database object which is imported by modules and controllers.
db = flask_sqlalchemy.SQLAlchemy(app)

# Register blueprints
from app.mod_main.controllers import mod_main as main_module
app.register_blueprint(main_module)

from app.mod_auth.controllers import mod_auth as auth_module
app.register_blueprint(auth_module)

from app.mod_self_statistics.controllers import mod_self_stats as stat_module
app.register_blueprint(stat_module)

from app.restapi import Root as RestRoot
app.register_blueprint(RestRoot, url_prefix='/api')

# Make sure to abort all attempts to access an unimplemented part of the API.
app.url_map.add(Rule('/api/<path:Path>', endpoint="unimplemented_restapi"))
@app.endpoint("unimplemented_restapi")
def unimplemented_restapi(Path=None):
    flask.abort(404)

'''
TODO:
- Move this somewhere else. Config file?
- Can we have multiple encoders (e.g., one for each model?)
'''
class OKJSONEncoder(flask.json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}

            for field in dir(obj):
                if (field.startswith('_')
                        or field.startswith('query')
                        or field == 'metadata'):
                    continue

                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                except TypeError:
                    try:
                        fields[field] = str(data)
                    except Exception:
                        fields[field] = None
                else:
                    fields[field] = data

            return fields

        return flask.json.JSONEncoder.default(self, obj)

app.json_encoder = OKJSONEncoder

# ================================== Logins ===================================

from app.mod_auth.models import User as _User

login_manager = flask_login.LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Since the user_id is just the primary key of our user table, use it in
    # the query for the user.
    return _User.query.get(int(user_id))
