import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from typing import List, Optional
from flaskblog import mail

def save_picture(form_picture, folder_path, output_size):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext

    picture_path = os.path.join(current_app.root_path, 'static', folder_path, picture_fn)
    form_picture.save(picture_path)

    # Ajustando o tamanho da imagem.
    image = Image.open(form_picture)
    image.thumbnail(output_size)
    image.save(picture_path)

    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        'Redefinição de Senha',
        sender='noreply@demo.com',
        recipients=[user.email]
    ) 

    msg.body = f'''Para redefinir sua senha, visite o seguinte link:
{url_for('users.reset_token', token=token, _external=True)}

Se você não solicitou essa alteração, apenas ignore este e-mail.'''

    mail.send(msg)

def get_pagination_list(
    current_page: int,
    total_pages: int,
    left_edge: int = 1,
    right_edge: int = 1,
    left_current: int = 1,
    right_current: int = 2
) -> List[Optional[int]]:
    
    items = []
    last_num = 0

    for num in range(1, total_pages + 1):
        if (
            num <= left_edge
            or num > total_pages - right_edge
            or (current_page - left_current <= num <= current_page + right_current)
        ):
            if last_num + 1 != num:
                items.append(None)
            
            items.append(num)
            last_num = num
            
    return items