from typing import List
from sqlalchemy.orm import Session
from flaskblog.models.comment import Comment

class CommentRepository:
    # Inicializando repositorio com a sessão do banco de dados
    def __init__(self, session: Session):
        self.session = session

    # Método Create
    def add_comment(self, comment: Comment) -> Comment:
        self.session.add(comment)
        self.session.commit()
        # Refresh para pegar o ID gerado e datas de criação
        self.session.refresh(comment)
        return comment

    # Métodos Read
    def list_comments_by_product_id(self, product_id: int, limit: int, offset: int) -> List[Comment]:
        return self.session.query(Comment)\
                    .filter(Comment.product_id == product_id)\
                    .order_by(Comment.time_created.desc())\
                    .limit(limit)\
                    .offset(offset)\
                    .all()
    
    # Count: necessário para paginação
    def count_comments_by_product_id(self, product_id: int) -> int:
        return self.session.query(Comment).filter(Comment.product_id == product_id).count()
    
    # Count por id de usuário: Query de filtro
    def get_comment_by_user_id(self, user_id: int, limit: int, offset: int) -> List[Comment]:
        return self.session.query(Comment)\
                    .filter(Comment.user_id == user_id)\
                    .limit(limit)\
                    .offset(offset)\
                    .all()

    # Count: necessário para paginação
    def count_comments_by_user_id(self, user_id: int) -> int:
        return self.session.query(Comment).filter(Comment.user_id == user_id).count()
    
    def get_comment_by_id(self, comment_id: int) -> int:
        return self.session.query(Comment).get(comment_id)
    
    # Método Update
    def update_comment(self, comment: Comment) -> Comment:
        comment = self.session.merge(comment)
        self.session.commit()
        self.session.refresh(comment)
        return comment

    # Método Delete
    def delete_comment(self, comment: Comment) -> None:
        self.session.delete(comment)
        self.session.commit()