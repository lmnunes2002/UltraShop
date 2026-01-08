from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'e6dc8ff8d1fa2d2df0a2b278a3646ec4'

database_uri = app.config.get('DATABASE_URL', 'sqlite:///site.db')
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False


from flaskblog import routes
