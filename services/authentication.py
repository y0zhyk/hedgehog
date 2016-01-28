from flask import Blueprint, request, redirect, session
from datetime import datetime
from jinja2 import Template

authentication = Blueprint('authentication', __name__)

LOGIN_FORM = \
    '''
    {% if error %}
    <span>{{error}}</span>
    {% endif %}
    <form method="post" action="/api/login">
        <input type="password" name="password" placeholder="Password">
        <input type="submit" name="submit" value="Login">
    </form>
    '''

error = None


@authentication.route('/api/login', methods=['POST', 'GET'])
def login():
    global error
    if request.method == 'POST':
        password = request.form['password']
        result, error = authenticate_user('yozhyk', password)
        if result:
            session['auth-ticket'] = generate_auth_ticket()
        return redirect('/')
    login_form = Template(LOGIN_FORM).render(error=error)
    error = None
    return login_form


@authentication.route('/api/logout')
def logout():
    session.pop('auth-ticket', None)
    return redirect('/')


def authenticate_user(username, password):
    try:
        import pam
        if pam.authenticate(username, password):
            return True, None
        else:
            return False, "Incorrect password"
    except ImportError:
        return False, "Authentication modules is not available"


def generate_auth_ticket():
    return str(int(datetime.now().timestamp()))


def is_auth_ticket_valid(auth_ticket):
    return 0 <= int(datetime.now().timestamp()) - int(auth_ticket) < 15 * 60  # 15 minutes


def is_session_authenticated():
    if 'auth-ticket' in session:
        return is_auth_ticket_valid(session['auth-ticket'])
    return False
