from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import IntegerField, DecimalField, StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class ProductForm(FlaskForm):
    title = StringField('Título do Produto', 
        validators=[DataRequired(message='O título do produto é obrigatório.'),
        Length(min=2, max=100, message='O título deve ter entre 2 e 100 caracteres.')]
    )

    description = TextAreaField('Descrição do Produto',
        validators=[DataRequired(message='A descrição do produto é obrigatória.'),
        Length(min=10, max=500, message='A descrição deve ter entre 10 e 500 caracteres.')]
    )

    price = DecimalField('Preço do Produto (R$)',
        validators=[DataRequired(message='O preço do produto é obrigatório.'),
        NumberRange(min=0.01, message='O preço deve ser positivo.')]
    )

    picture = FileField('Foto do Produto',
        validators= [DataRequired(message='A foto do produto é obrigatória.'),
        FileAllowed(['jpg', 'png'], 'Apenas imagens JPG e PNG são permitidas!')]
    )

    quantity = IntegerField('Quantidade em Estoque', 
        validators=[DataRequired(),
        NumberRange(min=1, message="O cadastro deve ser de pelo menos 1 unidade.")],
        default=1)
    
    condition = SelectField('Condição do Produto', 
        choices=[('Novo', 'Novo'), ('Seminovo', 'Seminovo'), ('Usado', 'Usado')],
        validators=[DataRequired()])
    
    status = SelectField('Status do Anúncio', 
        choices=[('Ativo', 'Ativo'), ('Reservado', 'Reservado'), ('Vendido', 'Vendido')],
        default='Ativo')

    submit = SubmitField('Cadastrar Produto')

class UpdateProductForm(FlaskForm):
    title = StringField('Título do Produto', 
        validators=[DataRequired(message='O título do produto é obrigatório.'),
        Length(min=2, max=100, message='O título deve ter entre 2 e 100 caracteres.')]
    )

    description = TextAreaField('Descrição do Produto',
        validators=[DataRequired(message='A descrição do produto é obrigatória.'),
        Length(min=10, max=500, message='A descrição deve ter entre 10 e 500 caracteres.')]
    )

    price = DecimalField('Preço do Produto (R$)',
        validators=[DataRequired(message='O preço do produto é obrigatório.'),
        NumberRange(min=0.01, message='O preço deve ser positivo.')]
    )

    picture = FileField('Foto do Produto',
        validators= [Optional(),
        FileAllowed(['jpg', 'png'], 'Apenas imagens JPG e PNG são permitidas!')]
    )

    quantity = IntegerField('Quantidade em Estoque', 
        validators=[DataRequired(),
        NumberRange(min=1, message="O cadastro deve ser de pelo menos 1 unidade.")],
        default=1)
    
    condition = SelectField('Condição do Produto', 
        choices=[('Novo', 'Novo'), ('Seminovo', 'Seminovo'), ('Usado', 'Usado')],
        validators=[DataRequired()])
    
    status = SelectField('Status do Anúncio', 
        choices=[('Ativo', 'Ativo'), ('Reservado', 'Reservado'), ('Vendido', 'Vendido')],
        default='Ativo')

    submit = SubmitField('Atualizar Produto')