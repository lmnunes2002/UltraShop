from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import DecimalField, StringField, SubmitField, TextAreaField
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

    submit = SubmitField('Atualizar Produto')