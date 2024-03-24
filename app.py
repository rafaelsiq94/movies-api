import flask
from flask import Flask

from src.routes import movies
from database import init_db
import config.settings as settings

init_db()

app = Flask(__name__)
flask.json.provider.DefaultJSONProvider.sort_keys = False
if settings.DEVELOPMENT:
    app.debug = True

app.register_blueprint(movies)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001)
