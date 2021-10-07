import flask
import flask_login
from werkzeug.security import generate_password_hash, check_password_hash

from app import db as _db
import app.mod_auth.models as _models

mod_auth = flask.Blueprint('auth', __name__)

# @mod_auth.route('/signup')
# def signup():
#     return flask.render_template('authorization/signup.html')

# @mod_auth.route('/signup', methods=['POST'])
# def signup_post():
#     user_details = {
#         'email': flask.request.form.get('email'),
#         'name': flask.request.form.get('name'),
#         'password': generate_password_hash(
#             flask.request.form.get('password'),
#             method='sha256',
#         ),
#     }

#     # If a user is found, we want to redirect back to signup page so user can
#     # try again.
#     for attr, str in (('name', 'Username'), ('email', 'Email address')):
#         kwargs = {attr: user_details[attr]}
#         if _models.User.query.filter_by(**kwargs).first() is not None:
#             flask.flash('{} already exists.'.format(str))

#     # Create a new user with the form data. Hash the password so the plaintext
#     # version isn't saved.
#     new_user = _models.User(**user_details)

#     # Add the new user to the database.
#     _db.session.add(new_user)
#     _db.session.commit()

#     return flask.redirect(flask.url_for('auth.login'))

@mod_auth.route('/login')
def login():
    return flask.render_template('authorization/login.html')

@mod_auth.route('/login', methods=['POST'])
def login_post():
    email = flask.request.form.get('email')
    password = flask.request.form.get('password')

    user = _models.User.query.filter_by(email=email).first()

    # If the user doesn't exist or is using the wrong password, we want to
    # display a message and reload the page.
    if not user or not check_password_hash(user.password, password):
        flask.flash('Please check your login details and try again.')
        return flask.redirect(flask.url_for('auth.login'))

    flask_login.login_user(user)
    return flask.redirect(flask.url_for('self_stats.control'))

@mod_auth.route('/logout')
def logout():
    return 'Logout'
