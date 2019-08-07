# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, g, session, redirect, url_for

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_sketch = Blueprint('sketch', __name__, url_prefix='/sketch')

# Set the route and accepted methods
@mod_sketch.route('/')
def sketch():
    return render_template("sketch/sketch.html")
