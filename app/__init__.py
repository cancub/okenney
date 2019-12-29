# Import flask and template operators
from flask import Flask, render_template
from flask_restful import Resource, Api
import mysql.connector as mariadb

# Define the WSGI application object
app = Flask(__name__)
api = Api(app)

# Configurations
app.config.from_object('config')

mariadb_connection = mariadb.connect(**app.config['DATABASE_CONNECT_OPTIONS'])
cursor = mariadb_connection.cursor()

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_sketch.controllers import mod_sketch as sketch_module

# API stuff
from app.rest_api.sketch import ImageMeta 

# Register blueprint(s)
app.register_blueprint(sketch_module)

api.add_resource(ImageMeta, '/api/image', '/api/image/<string:filename>')

# app.register_blueprint(xyz_module)
# ..

@app.route('/')
def index():
    # find the most recent article
    cursor.execute('SELECT fpath FROM main ORDER BY datetime DESC LIMIT 1')
    return render_template(cursor.next()[0])

@app.route('/articles/<name>')
def article(name):
    # use mysql to find location
    return render_template()
