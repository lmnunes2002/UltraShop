from flask import render_template, flash, redirect, url_for
from flaskblog import app, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Product
from flaskblog.infra.connection import db

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
        if (form.login.data == 'Lucas' or form.login.data == 'lucas@demo.com') and form.password.data == '123456':
            flash(f'Você está logado em {form.login.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Login inválido. Por favor, verifique sua credencial e senha.', 'danger')
    return render_template('login.html', title='Login', form=form)