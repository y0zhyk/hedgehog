from flask import Blueprint, request, redirect, session, escape


authentication = Blueprint('authentication', __name__)


@authentication.route('/login', methods=['POST'])
def login():
    password = request.form['password']
    if 'password' == password:
        session['ticket'] = '000'
        return redirect('/home')
    return redirect('/home')

@authentication.route('/logout')
def logout():
    session.pop('ticket', None)
    return redirect('/home')

def is_valid_ticket(ticket):
    return ticket == '000'


def is_session_authenticated():
    if 'ticket' in session:
        return is_valid_ticket(session['ticket'])
    return False