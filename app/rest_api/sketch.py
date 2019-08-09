import os
from PIL import Image

import flask
from flask_restful import Resource
from flask import current_app as Main

class ImageMeta(Resource):
    def get(self, filename):
        filepath = os.path.join(Main.root_path, 'static', 'images', filename)
        with Image.open(filepath) as img:
            width, height = img.size
        return flask.jsonify({'width': width, 'height': height})
