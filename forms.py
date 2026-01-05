from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
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

class LoginForm(FlaskForm):
    login = StringField('E-mail ou Usuário',
        validators=[DataRequired(message="Por favor, insira seu e-mail ou nome de usuário.")]
    )

    password = PasswordField('Senha',
        validators=[DataRequired(message="Por favor, insira sua senha.")]
    )

    remember = BooleanField('Lembre-se de mim')
    submit = SubmitField('Login')