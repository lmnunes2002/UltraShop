from flask_wtf import FlaskForm
from wtforms import TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class BaseCommentForm(FlaskForm):
        content = TextAreaField('Comentário',
        validators=[DataRequired(),
        Length(min=1, max=300)])

class CommentForm(BaseCommentForm):
    stars = SelectField('Avaliação',
        choices=[(5, '⭐⭐⭐⭐⭐ (Excelente)'),
        (4, '⭐⭐⭐⭐ (Muito Bom)'),
        (3, '⭐⭐⭐ (Bom)'),
        (2, '⭐⭐ (Ruim)'),
        (1, '⭐ (Péssimo)')],
        coerce=int,
        validators=[DataRequired(message='A avaliação é obrigatória.')])
    
    submit = SubmitField('Enviar Comentário')

class UpdateCommentForm(BaseCommentForm):
    stars = SelectField('Avaliação',
        choices=[(5, '⭐⭐⭐⭐⭐ (Excelente)'),
        (4, '⭐⭐⭐⭐ (Muito Bom)'),
        (3, '⭐⭐⭐ (Bom)'),
        (2, '⭐⭐ (Ruim)'),
        (1, '⭐ (Péssimo)')],
        coerce=int,
        validators=[Optional()])
    
    submit = SubmitField('Atualizar Comentário')