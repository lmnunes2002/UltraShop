import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import app, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProductForm
from flaskblog.models import User, Product
from flaskblog.repositories import UserRepository, ProductRepository
from flaskblog.infra.connection import db

@app.route('/')
@app.route('/home')
def home():
    repo = ProductRepository(db)
    products = repo.list_products()
    return render_template('home.html', products=products)

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

def save_picture(form_picture, folder_path):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(app.root_path, 'static', folder_path, picture_fn)
    form_picture.save(picture_path)

    # Ajustando o tamanho da imagem.
    output_size = (125, 125)
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
            picture_file = save_picture(form.picture.data, 'profile_pics')
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
        product_image_file = save_picture(form.picture.data, 'product_pics')

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
    return render_template('create_product.html', title='Novo Produto', form=form)