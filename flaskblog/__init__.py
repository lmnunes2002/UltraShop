from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.infra.connection import db, engine, Base

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e6dc8ff8d1fa2d2df0a2b278a3646ec4'

database_uri = app.config.get('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@app.teardown_appcontext
def shutdown_session(exception=None):
    db.remove()
    print("Sessão encerrada.")

with app.app_context():
    Base.metadata.create_all(bind=engine)

from flaskblog import routes
