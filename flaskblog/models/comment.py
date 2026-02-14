from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from flaskblog.infra.connection import Base

class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    stars = Column(Integer, nullable=False)

    # Timestamps
    time_created = Column(DateTime(timezone=True), default=datetime.now)
    time_updated = Column(DateTime(timezone=True), onupdate=datetime.now, default=datetime.now)

    # Chaves estrangeiras do User e Product
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)

    # Metódo mágica para representar e debugar
    def __repr__(self):
        return f'(Comentário: {self.content} - Usuário ID: {self.user_id} - Produto ID: {self.product_id})'