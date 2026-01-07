from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infra.connection import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(60), nullable=False)
    img_file = Column(String(20), nullable=False, default='default.jpg')

    # Timestamps
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

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