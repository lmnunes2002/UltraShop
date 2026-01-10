from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base

# Cria o objeto Base para os modelos herdarem
Base = declarative_base()

# Definição da URL de conexão com o banco de dados SQLite
DATABASE_URL = 'sqlite:///site.db'

# Criação da engine de conexão
# String de conexão do sqlite (usa driver interno)
# Habilita logging de SQL para debug
# Necessário para SQLite com múltiplas threads
engine = create_engine(
    DATABASE_URL,    
    echo=True,              
    connect_args={"check_same_thread": False}
)

# Cria uma sessão configurada para interagir com o banco de dados
session_factory = sessionmaker(bind=engine)

db = scoped_session(session_factory)