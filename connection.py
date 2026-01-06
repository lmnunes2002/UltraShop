from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Definição da URL de conexão com o banco de dados SQLite
DATABASE_URL = 'sqlite:///site.db'

# Criação da engine de conexão
# String de conexão do sqlite (usa driver interno)
# Habilita logging de SQL para debug
# Necessário para SQLite com múltiplas threads
engine = create_engine(
    'sqlite:///site.db',    
    echo=True,              
    connect_args={"check_same_thread": False}
)

# Cria o objeto Base para os modelos herdarem
Base = declarative_base()

# Cria uma sessão configurada para interagir com o banco de dados
SessionLocal = sessionmaker(bind=engine)