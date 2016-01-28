from functools import wraps
from flask import Blueprint, render_template, redirect
from services.authentication import is_session_authenticated
from .tiles import tiles

hedgehog = Blueprint('hedgehog', __name__)


def requires_authentication(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_session_authenticated():
            return login()
        return func(*args, **kwargs)

    return wrapper


@hedgehog.route('/')
@hedgehog.route('/home')
@requires_authentication
def home():
    return render_template('home.html', tiles=tiles(is_session_authenticated=True))


@hedgehog.route('/login')
def login():
    if is_session_authenticated():
        return redirect('/')
    return render_template('home.html', tiles=tiles(is_session_authenticated=False))
