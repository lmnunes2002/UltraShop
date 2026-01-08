from flaskblog.infra.connection import engine, Base
from flaskblog.models.user import User
from flaskblog.models.product import Product

# Só rodar uma vez!!!
def create_database():
    print("Conectando ao banco de dados...")
    
    # Dropa todas as tabelas registradas no Base
    Base.metadata.drop_all(bind=engine)
    # Cria todas as tabelas registradas no Base
    Base.metadata.create_all(bind=engine)
    
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    create_database()