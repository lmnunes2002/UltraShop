import os
import secrets
from flask import current_app
from PIL import Image

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