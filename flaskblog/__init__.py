from flask import Flask, app
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.infra.connection import db, engine, Base
from flaskblog.config import Config

mail = Mail()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    mail.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.remove()
        print("Sessão encerrada.")

    with app.app_context():
        Base.metadata.create_all(bind=engine)

    # Importando cada blueprint
    from flaskblog.blueprints.users.routes import users
    from flaskblog.blueprints.products.routes import products
    from flaskblog.blueprints.errors.handlers import errors
    from flaskblog.blueprints.main.routes import main

    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(errors)
    app.register_blueprint(main)

    return app