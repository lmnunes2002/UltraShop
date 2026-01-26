import os
import secrets
import math
from PIL import Image
from flask import render_template, flash, redirect, request, url_for, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from flaskblog import app, bcrypt, mail
from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                            ProductForm, RequestResetForm, ResetPasswordForm)
from flaskblog.models import User, Product
from flaskblog.repositories import UserRepository, ProductRepository
from flaskblog.infra.connection import db
from flaskblog.utils import get_pagination_list

@app.route('/')
@app.route('/home')
def home():
    # Configura produtos por página.
    PER_PAGE = 8
    page = request.args.get('page', 1, type=int)

    # Quantidade de itens à pular antes de paginar.
    offset = (page - 1) * PER_PAGE

    # Query de produtos.
    repo = ProductRepository(db)
    products = repo.list_products(limit=PER_PAGE, offset=offset)
    total_products = repo.count_products()

    # Divisão arredondada para cima do total de páginas.
    total_pages = math.ceil(total_products / PER_PAGE)

    # Lista de paginação.
    pagination_list = get_pagination_list(page, total_pages)

    return render_template(
        'home.html',
        products=products,
        page=page,
        total_pages=total_pages,
        pagination_list=pagination_list
    )

@app.route('/about')
def about():
    return render_template('about.html', title='Sobre nós')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        repo = UserRepository(db)
        repo.add_user(user)

        flash(f'Sua conta foi criada com sucesso, faça o login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Cadastro', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Entrada de dados de login.
        login_data = form.login.data
        repo = UserRepository(db)

        # Queries que encontram o usuário pelo e-mail ou nome de usuário.
        user = repo.get_user_by_email(login_data)

        if not user:
            user = repo.get_user_by_username(login_data)

        # Verificação de existência do usuário e validação da senha.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login realizado com sucesso! Bem-vindo(a), {user.username}.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Login inválido. Por favor, verifique sua credencial e senha.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture, folder_path, output_size):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(app.root_path, 'static', folder_path, picture_fn)
    form_picture.save(picture_path)

    # Ajustando o tamanho da imagem.
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data, 'profile_pics', (125, 125))
            current_user.image_file = picture_file

        current_user.username = form.username.data
        current_user.email = form.email.data
        repo = UserRepository(db)
        repo.update_user(current_user)

        flash('Sua conta foi atualizada com sucesso!', 'success')
        return redirect(url_for('account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Sua conta', image_file=image_file, form=form)

@app.route('/products/new', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product_image_file = save_picture(form.picture.data, 'product_pics', (1080, 1080))

        product = Product(
            name=form.title.data, 
            price=form.price.data, 
            description=form.description.data, 
            image_file=product_image_file, 
            author=current_user
        )

        repo = ProductRepository(db)
        repo.add_product(product)
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('home'))
    return render_template('create_product.html', title='Novo Produto', form=form, legend='Novo Produto')

@app.route('/products/<int:product_id>')
def product(product_id):
    repo = ProductRepository(db)
    product = repo.get_product_by_id(product_id)

    if product is None:
        abort(404)

    return render_template('product.html', title=product.name, product=product)

@app.route('/products/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    repo = ProductRepository(db)
    product = repo.get_product_by_id(product_id)

    if product.author != current_user:
        abort(403)

    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.title.data
        product.price = form.price.data
        product.description = form.description.data

        if form.picture.data:
            product_image_file = save_picture(form.picture.data, 'product_pics', (1080, 1080))
            product.image_file = product_image_file
        elif request.method == 'GET':
            form.title.data = product.name
            form.price.data = product.price
            form.description.data = product.description

        repo.update_product(product)
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('product', product_id=product.id))
    
    form.title.data = product.name
    form.price.data = product.price
    form.description.data = product.description
    return render_template('create_product.html', title='Atualizar Produto', form=form, legend='Atualizar Produto')

@app.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    repo = ProductRepository(db)
    product = repo.get_product_by_id(product_id)

    if product.author != current_user:
        abort(403)

    repo.delete_product(product)
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('home'))

@app.route('/users/<string:username>')
def user_products(username):
    PER_PAGE = 8
    page = request.args.get('page', 1, type=int)

    repo = UserRepository(db)
    user = repo.get_user_by_username(username)

    if user is None:
        abort(404)
        
    offset = (page - 1) * PER_PAGE

    repo = ProductRepository(db)
    products = repo.get_products_by_user_id(user.id, limit=PER_PAGE, offset=offset)
    total_products = repo.count_products_by_user_id(user.id)

    total_pages = math.ceil(total_products / PER_PAGE)

    pagination_list = get_pagination_list(page, total_pages)

    return render_template(
        'user_products.html',
        user=user,
        products=products,
        page=page,
        total_pages=total_pages,
        pagination_list=pagination_list,
        total_products=total_products
    )

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Redefinição de Senha',
        sender='noreply@demo.com',
        recipients=[user.email]
    ) 

    msg.body = f'''Para redefinir sua senha, visite o seguinte link:
{url_for('reset_token', token=token, _external=True)}

Se você não solicitou essa alteração, apenas ignore este e-mail.'''

    mail.send(msg)
    
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = RequestResetForm()

    if form.validate_on_submit():
        repo = UserRepository(db)
        user = repo.get_user_by_email(email=form.email.data)
        send_reset_email(user)
        flash('Um e-mail com instruções para redefinir sua senha foi enviado.', 'info')
        return redirect(url_for('login'))

    return render_template('reset_request.html', title='Redefinir Senha', form=form)

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    user = User.verify_reset_token(token)

    if user is None:
        flash('O token de redefinição de senha é inválido ou expirou.', 'warning')
        return redirect(url_for('reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password

        repo = UserRepository(db)
        repo.update_user(user)

        flash(f'Sua senha foi atualizada, faça o login!', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Redefinir Senha',form=form)