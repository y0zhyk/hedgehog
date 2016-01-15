from flask import Flask
from views.hedgehog import hedgehog
from views.autentication import authentication

app = Flask(__name__)
app.register_blueprint(hedgehog)
app.register_blueprint(authentication)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0", port=8080)
