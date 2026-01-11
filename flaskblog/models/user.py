from flaskblog import login_manager
from flaskblog.infra.connection import Base, db
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from flask_login import UserMixin
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
    img_file = Column(String(20), nullable=False, default='default.jpg')

    # Timestamps
    time_created = Column(DateTime(timezone=True), default=datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.now, default=datetime.now)

    # Relação 1 -> N com produtos
    products = relationship(
        'Product',
        back_populates='user',
        cascade='all, delete-orphan'
    )

    # Configuração para herança polimórfica
    type = Column(String(50), nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': 'type'
    }

    # Metódo mágico para representar e debugar
    def __repr__(self):
        return f'({self.username} - {self.email} - {self.img_file})'