from flask import Blueprint, render_template
from .tiles import tiles
from .autentication import is_session_authenticated

hedgehog = Blueprint('hedgehog', __name__)


@hedgehog.route('/')
@hedgehog.route('/home')
def home():
    is_user_authenticated = is_session_authenticated()
    current_tiles = tiles(is_user_authenticated)
    return render_template('home.html', tiles=current_tiles)
