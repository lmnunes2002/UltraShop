from flaskblog import app, login_manager
from flaskblog.infra.connection import Base, db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return db.get(User, int(user_id))

class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    image_file = Column(String(20), nullable=False, default='default.jpg')

    # Timestamps
    time_created = Column(DateTime(timezone=True), default=datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.now, default=datetime.now)

    # Relação 1 -> N com produtos
    products = relationship(
        'Product',
        backref='author',
        lazy=True,
        cascade='all, delete-orphan'
    )

    # Configuração para herança polimórfica
    type = Column(String(50), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type'
    }

    def get_reset_token(self):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token):
        s = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token, salt='password-reset-salt', max_age=1800)
        except:
            return None

        user_id = data['user_id']
        return db.get(User, user_id)

    # Metódo mágico para representar e debugar
    def __repr__(self):
        return f'({self.username} - {self.email} - {self.image_file})'