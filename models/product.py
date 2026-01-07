from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from infra.connection import Base

class Product(Base):
    __tablename__ = 'products'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    author = Column(String(50), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(500), nullable=False)
    price = Column(Float, nullable=False)
    img_file = Column(String(20), nullable=False, default='product_default.jpg')

    # Chave estrangeira da tabela de usuários
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    # Relacionameto com o usuário
    user = relationship('User', back_populates='products')

    # Timestamps
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())

    # Metódo mágico para representar e debugar
    def __repr__(self):
        return f'({self.name} - {self.price} - {self.img_file} - {self.user_id})'