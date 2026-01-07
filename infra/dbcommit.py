# PARTE 1: Importar a Base e a Sessão
from models.user import User 
from models.product import Product 
from infra.connection import SessionLocal

# PARTE 2: Criar a sessão (instanciar o db)
db = SessionLocal()

# PARTE 3: Criar o objeto user
while True:
    answer_user = input('Deseja criar um novo usuário? (s/n): ').strip().lower()

    if answer_user == 's':
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

        # PARTE 4: Criar o objeto product
        while True:
            answer_product = input('Deseja criar um produto para este usuário? (s/n): ').strip().lower()

            if answer_product == 's':
                product_name = input('Digite o nome do produto: ').strip()
                description = input('Digite a descrição do produto: ').strip()
                price = float(input('Digite o preço do produto: ').strip())
                img_file = input('Digite o nome do arquivo de imagem do produto: ').strip() or 'product_default.jpg'

                product = Product(
                    author=username,
                    name=product_name,
                    description=description,
                    price=price,
                    img_file=img_file,
                    user=user
                )

                # PARTE 5: Add e Commit product
                db.add(product)
                db.commit()
                print(f'Produto {product_name} criado para o usuário {username} com sucesso!')
            else:
                break

        # PARTE 6: Add e Commit user
        db.add(user)
        db.commit()
        print(f'Usuário {username} criado com sucesso!')
    else:
        print('Encerrando a criação de usuários.')
        break