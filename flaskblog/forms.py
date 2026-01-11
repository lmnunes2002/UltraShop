from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User

# Formulário de Registro de Usuário.
class RegistrationForm(FlaskForm):
    # Campos com validações
    username = StringField('Nome de Usuário', 
        validators=[DataRequired(message="O nome de usuário é obrigatório."),
        Length(min=2, max=50, message="O nome deve ter entre 2 e 50 caracteres.")]
    )

    email = StringField('E-mail',
        validators=[DataRequired(message="O e-mail é obrigatório"),
        Email(message="Formato de e-mail inválido.")]
    )

    password = PasswordField('Senha',
        validators=[DataRequired(message="A senha não pode estar vazia."),
        Length(min=6, message="A senha deve ter pelo menos 6 caracteres.")]
    )

    password_confirm = PasswordField('Confirmar Senha',
        validators=[DataRequired(message="Confirme sua senha."),
        EqualTo('password', message='As senhas devem ser iguais.')]
    )

    submit = SubmitField('Registrar')

    # Templates de validação personalizada.
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()

        if user:
            raise ValidationError('Este nome de usuário já está em uso. Por favor, escolha outro.')

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()

        if user:
            raise ValidationError('Este e-mail já está em uso. Por favor, escolha outro.')            

# Formulário de Login de Usuário.
class LoginForm(FlaskForm):
    # Campos com validações
    login = StringField('E-mail ou Usuário',
        validators=[DataRequired(message="Por favor, insira seu e-mail ou nome de usuário.")]
    )

    password = PasswordField('Senha',
        validators=[DataRequired(message="Por favor, insira sua senha.")]
    )

    remember = BooleanField('Lembre-se de mim')
    submit = SubmitField('Login')