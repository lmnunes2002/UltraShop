from typing import List, Optional
from sqlalchemy.orm import Session
from flaskblog.models.user import User
from flaskblog.users.utils import delete_picture

class UserRepository:
    # Inicializando repositorio com a sessão do banco de dados
    def __init__(self, session: Session):
        self.session = session

    # Método Create
    def add_user(self, user: User) -> User:
        self.session.add(user)
        self.session.commit()
        # Refresh para pegar o ID gerado e datas de criação
        self.session.refresh(user)
        return user

    # Métodos Read
    def list_users(self) -> List[User]:
        return self.session.query(User.time_created.desc())\
            .order_by(User)\
            .all()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.session.query(User).filter(User.id == user_id).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(User.username == username).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(User.email == email).first()
    
    # Método Update
    def update_user(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user

    # Método Delete
    def delete_user(self, user: User) -> None:
        # Armazena o nome da imagem antes de deletar o produto do banco.
        image_file = user.image_file

        if image_file:
            delete_picture(image_file, 'profile_pics')

        # Deleta as imagens dos produtos associados ao usuário
        for product in user.products:
            if product.image_file:
                delete_picture(product.image_file, 'product_pics')
 
        self.session.delete(user)
        self.session.commit()