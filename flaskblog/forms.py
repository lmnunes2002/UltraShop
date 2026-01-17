from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flaskblog.infra.connection import db

# Formulário de Registro de Usuário.
class RegistrationForm(FlaskForm):
    # Campos com validações
    username = StringField('Nome de Usuário', 
        validators=[DataRequired(message='O nome de usuário é obrigatório.'),
        Length(min=2, max=50, message='O nome deve ter entre 2 e 50 caracteres.')]
    )

    email = StringField('E-mail',
        validators=[DataRequired(message='O e-mail é obrigatório'),
        Email(message='Formato de e-mail inválido.')]
    )

    password = PasswordField('Senha',
        validators=[DataRequired(message='A senha não pode estar vazia.'),
        Length(min=6, message='A senha deve ter pelo menos 6 caracteres.')]
    )

    password_confirm = PasswordField('Confirmar Senha',
        validators=[DataRequired(message='Confirme sua senha.'),
        EqualTo('password', message='As senhas devem ser iguais.')]
    )

    submit = SubmitField('Registrar')

    # Templates de validação personalizada.
    def validate_username(self, username):
        user = db.query(User).filter_by(username=username.data).first()

        if user:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')

    def validate_email(self, email):
        user = db.query(User).filter_by(email=email.data).first()

        if user:
            raise ValidationError('Este e-mail já está em uso. Por favor, escolha outro.')            

# Formulário de Login de Usuário.
class LoginForm(FlaskForm):
    # Campos com validações
    login = StringField('E-mail ou Usuário',
        validators=[DataRequired(message='Por favor, insira seu e-mail ou nome de usuário.')]
    )

    password = PasswordField('Senha',
        validators=[DataRequired(message='Por favor, insira sua senha.')]
    )

    remember = BooleanField('Lembre-se de mim')
    submit = SubmitField('Login')

# Formulário de Atualização de Usuário.
class UpdateAccountForm(FlaskForm):
    # Campos com validações
    username = StringField('Nome de Usuário', 
        validators=[DataRequired(message='O nome de usuário é obrigatório.'),
        Length(min=2, max=50, message='O nome deve ter entre 2 e 50 caracteres.')]
    )

    email = StringField('E-mail',
        validators=[DataRequired(message='O e-mail é obrigatório'),
        Email(message='Formato de e-mail inválido.')]
    )

    picture = FileField('Atualizar Foto de Perfil',
        validators= [FileAllowed(['jpg', 'png'])]
    )

    submit = SubmitField('Atualizar')

    # Templates de validação personalizada.
    def validate_username(self, username):
        # Se já existe um usuário com o nome igual ao nome desejado, impossibilita a atualização.
        if username.data != current_user.username:
            user = db.query(User).filter_by(username=username.data).first()

            if user:
                raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')

    def validate_email(self, email):
        # Se já existe um usuário com o email igual ao nome desejado, impossibilita a atualização.
        if email.data != current_user.email:
            user = db.query(User).filter_by(email=email.data).first()

            if user:
                raise ValidationError('Este e-mail já está em uso. Por favor, escolha outro.')  

class ProductForm(FlaskForm):
    title = StringField('Título do Produto', 
        validators=[DataRequired(message='O título do produto é obrigatório.'),
        Length(min=2, max=100, message='O título deve ter entre 2 e 100 caracteres.')]
    )

    description = TextAreaField('Descrição do Produto',
        validators=[DataRequired(message='A descrição do produto é obrigatória.'),
        Length(min=10, max=500, message='A descrição deve ter entre 10 e 500 caracteres.')]
    )

    price = StringField('Preço do Produto',
        validators=[DataRequired(message='O preço do produto é obrigatório.')]
    )

    picture = FileField('Foto do Produto',
        validators= [DataRequired(message='A foto do produto é obrigatória.'),
        FileAllowed(['jpg', 'png'], 'Apenas imagens JPG e PNG são permitidas!')]
    )

    submit = SubmitField('Cadastrar Produto')