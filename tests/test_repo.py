from repositories.user_repository import UserRepository
from repositories.product_repository import ProductRepository
from infra.connection import Base, SessionLocal, engine
from models.user import User

session = SessionLocal(bind=engine)
user_repo = UserRepository(session)
product_repo = ProductRepository(session)

try:
    # Testando o Create
    user_teste = User(username="admin", email="admin@demo.com", password="qlegal")
    user_repo.add_user(user_teste)
    print(f"Usuário criado com ID: {user_teste.id}")

    # Testando o Read
    users = user_repo.list_users()
    print(f"Total de usuários no banco: {len(users)}")

finally:
    session.close()