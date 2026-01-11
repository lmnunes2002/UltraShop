from flask import render_template, flash, redirect, url_for
from flaskblog import app, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Product
from flaskblog.infra.connection import db
from flask_login import login_user, current_user, logout_user, login_required

products = [
    {
        'name': 'Laptop',
        'price': 999.99,
        'description': 'Um laptop de alto desempenho adequado para todas as suas necessidades de computação.',
        'author': 'Joãozinho',
        'date_posted': '20/08/2024'
    },
    {
        'name': 'Smartphone',
        'price': 499.99,
        'description': 'Um smartphone elegante com os recursos mais recentes e uma bela tela.',
        'author': 'Mariazinha',
        'date_posted': '15/09/2024'
    }
]

@app.route('/')
@app.route('/home')
def home():
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
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.add(user)
        db.commit()
        flash(f'Sua conta foi criada com sucesso, faça o login!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Cadastro', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Entrada de dados de login.
        login_data = form.login.data

        # Queries que encontram o usuário pelo e-mail ou nome de usuário.
        user = db.query(User).filter_by(email=login_data).first()

        if not user:
            user = db.query(User).filter_by(username=login_data).first()

        # Verificação de existência do usuário e validação da senha.
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash(f'Login realizado com sucesso! Bem-vindo(a) {user.username}.', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login inválido. Por favor, verifique sua credencial e senha.', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html', title='Sua conta')