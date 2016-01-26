from flask import Blueprint, request, redirect, session

authentication = Blueprint('authentication', __name__)


@authentication.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return generate_login_form()
    password = request.form['password']
    if 'password' == password:
        session['ticket'] = '000'
        return redirect('/home')
    return redirect('/home')


@authentication.route('/logout')
def logout():
    session.pop('ticket', None)
    return redirect('/home')


def generate_login_form():
    return


def is_valid_ticket(ticket):
    return ticket == '000'


def is_session_authenticated():
    if 'ticket' in session:
        return is_valid_ticket(session['ticket'])
    return False

