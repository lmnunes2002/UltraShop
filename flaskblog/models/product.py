from flaskblog.infra.connection import Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    image_file = Column(String(20), nullable=False, default='product_default.jpg')

    # Chave estrangeira da tabela de usuários
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Timestamps
    time_created = Column(DateTime(timezone=True), default=datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.now, default=datetime.now)

    # Metódo mágico para representar e debugar
    def __repr__(self):
        return f'({self.name} - {self.price} - {self.image_file} - {self.user_id})'