# PARTE 1: Importar a Base e a Sessão
from app.models.user import User 
from app.connection import SessionLocal

# Precisa importar o Product para criar o um usuário
from app.models.product import Product 

# PARTE 2: Criar a sessão (instanciar o db)
db = SessionLocal()

# PARTE 3: Criar o objeto user
while True:
    answer = input('Deseja criar um novo usuário? (s/n): ').strip().lower()

    if answer == 's':
        username = input('Digite o nome de usuário: ').strip()
        email = input('Digite o e-mail: ').strip()
        password = input('Digite a senha: ').strip()

        user = User(
            username=username,
            email=email,
            password=password,
            img_file='default.jpg',
            type='user'
        )

        db.add(user)
        db.commit()
        print(f'Usuário {username} criado com sucesso!')
    else:
        print('Encerrando a criação de usuários.')
        break

# PARTE 4: Add e Commit (A mágica acontece aqui)
db.add(user)
db.commit()