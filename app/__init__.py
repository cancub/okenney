# Import flask and template operators
from flask import Flask, render_template
from flask_restful import Resource, Api

# Import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)
api = Api(app)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_sketch.controllers import mod_sketch as sketch_module

# API stuff
from app.rest_api.sketch import ImageMeta 

# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(sketch_module)

api.add_resource(ImageMeta, '/api/image', '/api/image/<string:filename>')

# app.register_blueprint(xyz_module)
# ..

# Build the database:
# This will create the database file using SQLAlchemy
db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/en/')
def main():
    return render_template('index.html')
