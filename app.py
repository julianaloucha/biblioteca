from flask import Flask
from flask_cors import CORS
from api.monitorias import monitorias_blueprint
from api.users import users_blueprint

app = Flask(__name__)
CORS(app)

app.register_blueprint(monitorias_blueprint, url_prefix='/api')
app.register_blueprint(users_blueprint, url_prefix='/api')

if __name__ == '__main__':
    from os import environ
    from werkzeug.serving import run_simple

    if environ.get("WERKZEUG_RUN_MAIN") == "true":
        app.debug = True
    run_simple('localhost', 5000, app, use_debugger=True, use_reloader=True)
