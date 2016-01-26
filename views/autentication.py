from string import Template

from flask import Blueprint, request, redirect, session

authentication = Blueprint('authentication', __name__)
authentication_error = ""


@authentication.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'GET':
        return generate_login_form()
    password = request.form['password']
    if 'password' == password:
        session['ticket'] = '000'
        return redirect('/home')
    global authentication_error
    authentication_error = "Incorrect password"
    return redirect('/home')


@authentication.route('/logout')
def logout():
    session.pop('ticket', None)
    return redirect('/home')


def generate_login_form():
    error = ""
    global authentication_error
    if authentication_error:
        error = authentication_error
        authentication_error = ""
    template = '<svg><polygon points="0,0 100,0 150,75 100,150 0,150"/></svg>' \
               '<img src="static/images/password.png">' \
               '<form method="post" action="login">' \
               '<span class="error" hidden>$error</span>' \
               '<input type="password" name="password" value placeholder="Password">' \
               '<input type="submit" name="submit" value>' \
               '</form>' \
               '<script>' \
               ' (function() { $$(document).ready(function() { return showErrorMessage(); }); }).call(this);' \
               '</script>'
    return Template(template).substitute(error=error)

def is_valid_ticket(ticket):
    return ticket == '000'


def is_session_authenticated():
    if 'ticket' in session:
        return is_valid_ticket(session['ticket'])
    return False

