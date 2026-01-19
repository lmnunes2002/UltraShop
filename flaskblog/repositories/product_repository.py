from flaskblog.models.product import Product
from sqlalchemy.orm import Session
from typing import List, Optional

class ProductRepository:
    # Inicializando repositorio com a sessão do banco de dados
    def __init__(self, session: Session):
        self.session = session

    # Método Create
    def add_product(self, product: Product) -> Product:
        self.session.add(product)
        self.session.commit()
        # Refresh para pegar o ID gerado e datas de criação
        self.session.refresh(product)
        return product

    # Métodos Read
    def list_products(self, limit: int, offset: int) -> List[Product]:
        return self.session.query(Product)\
                    .limit(limit)\
                    .offset(offset)\
                    .all()

    # Count: necessário para paginação
    def count_products(self) -> int:
        return self.session.query(Product).count()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.session.query(Product).filter(Product.id == product_id).first()

    def get_products_by_user_id(self, user_id: int) -> List[Product]:
        return self.session.query(Product).filter(Product.user_id == user_id).all()

    # Método Update
    def update_product(self, product: Product) -> Product:
        self.session.commit()
        self.session.refresh(product)
        return product

    # Método Delete
    def delete_product(self, product: Product) -> None:
        self.session.delete(product)
        self.session.commit()