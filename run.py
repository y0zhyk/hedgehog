from flask import Flask
from views.hedgehog import hedgehog

app = Flask(__name__)
app.register_blueprint(hedgehog)


if __name__ == '__main__':
    app.debug = False
    app.run(host="0.0.0.0")