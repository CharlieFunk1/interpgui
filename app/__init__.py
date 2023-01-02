from flask import Flask
from config import Config
from flask_colorpicker import colorpicker
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)
colorpicker = colorpicker(app)

from app import routes, models

if __name__ == '__main__':
    socketio.run(app)
