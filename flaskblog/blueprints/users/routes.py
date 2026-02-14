import math
from flask import Blueprint, render_template, flash, redirect, request, url_for, abort
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import bcrypt
from flaskblog.infra.connection import db
from flaskblog.repositories import UserRepository, ProductRepository, CommentRepository
from flaskblog.models import User
from flaskblog.blueprints.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                            RequestResetForm, ResetPasswordForm)
from flaskblog.blueprints.users.utils import save_picture, send_reset_email, get_pagination_list

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
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
        return redirect(url_for('users.login'))
    return render_template('register.html', title='Cadastro', form=form)

@users.route('/login', methods=['GET', 'POST'])
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
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash(f'Login inválido. Por favor, verifique sua credencial e senha.', 'danger')
    return render_template('login.html', title='Login', form=form)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route('/account', methods=['GET', 'POST'])
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
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Sua conta', image_file=image_file, form=form)

@users.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
def delete_user(user_id):
    repo = UserRepository(db)
    user = repo.get_user_by_id(user_id)

    if user != current_user:
        abort(403)

    repo.delete_user(user)
    flash('Sua conta foi deletada com sucesso!', 'success')
    return redirect(url_for('main.home'))

@users.route('/users/<string:username>/products')
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

@users.route('/users/<string:username>/comments')
@login_required
def user_comments(username):
    PER_PAGE = 8
    page = request.args.get('page', 1, type=int)

    repo = UserRepository(db)
    user = repo.get_user_by_username(username)

    if user is None:
        abort(404)
        
    offset = (page - 1) * PER_PAGE

    repo = CommentRepository(db)
    comments = repo.get_comment_by_user_id(user.id, limit=PER_PAGE, offset=offset)
    total_comments = repo.count_comments_by_user_id(user.id)

    total_pages = math.ceil(total_comments / PER_PAGE)

    pagination_list = get_pagination_list(page, total_pages)

    return render_template(
        'user_comments.html',
        user=user,
        comments=comments,
        page=page,
        total_pages=total_pages,
        pagination_list=pagination_list,
        total_comments=total_comments
    )

@users.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()

    if form.validate_on_submit():
        repo = UserRepository(db)
        user = repo.get_user_by_email(email=form.email.data)
        send_reset_email(user)
        flash('Um e-mail com instruções para redefinir sua senha foi enviado.', 'info')
        return redirect(url_for('users.login'))

    return render_template('reset_request.html', title='Redefinir Senha', form=form)

@users.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token)

    if user is None:
        flash('O token de redefinição de senha é inválido ou expirou.', 'warning')
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password

        repo = UserRepository(db)
        repo.update_user(user)

        flash(f'Sua senha foi atualizada, faça o login!', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Redefinir Senha',form=form)