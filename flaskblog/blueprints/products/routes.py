import math
from flask import Blueprint, render_template, flash, redirect, request, url_for, abort
from flask_login import current_user, login_required
from flaskblog.infra.connection import db
from flaskblog.repositories import ProductRepository, CommentRepository
from flaskblog.models import Product
from flaskblog.blueprints.products.forms import ProductForm, UpdateProductForm
from flaskblog.blueprints.comments.forms import CommentForm
from flaskblog.blueprints.products.utils import save_picture, delete_picture, get_pagination_list

products = Blueprint('products', __name__)

@products.route('/products/new', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product_image_file = save_picture(form.picture.data, 'product_pics', (1080, 1080))

        product = Product(
            name=form.title.data, 
            price=form.price.data, 
            description=form.description.data,
            quantity=form.quantity.data,     
            condition=form.condition.data,   
            status=form.status.data,
            image_file=product_image_file, 
            author=current_user
        )

        repo = ProductRepository(db)
        repo.add_product(product)
        flash('Produto criado com sucesso!', 'success')
        return redirect(url_for('main.home'))
    return render_template('create_product.html', title='Novo Produto', form=form, legend='Novo Produto')

@products.route('/products/<int:product_id>')
def product(product_id):
    # Configuração comentários por página.
    PER_PAGE = 4
    page = request.args.get('page', 1, type=int)

    # Quantidade de itens à pular antes de paginar.
    offset = (page - 1) * PER_PAGE

    form = CommentForm()

    repo_product = ProductRepository(db)
    repo_comment = CommentRepository(db)

    product = repo_product.get_product_by_id(product_id)
    if product is None:
        abort(404)

    comments = repo_comment.list_comments_by_product_id(product_id, limit=PER_PAGE, offset=offset)
    total_comments = repo_comment.count_comments_by_product_id(product_id)

    # Divisão arredondada para cima do total de páginas.
    total_pages = math.ceil(total_comments / PER_PAGE)

    # Lista de paginação.
    pagination_list = get_pagination_list(page, total_pages)

    return render_template(
        'product.html',
        title=product.name,
        product=product,
        comments=comments,
        form=form,
        page=page,
        total_pages=total_pages,
        pagination_list=pagination_list
    )

@products.route('/products/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    repo = ProductRepository(db)
    product = repo.get_product_by_id(product_id)

    if product.author != current_user:
        abort(403)

    form = UpdateProductForm()

    if form.validate_on_submit():
        product.name = form.title.data
        product.price = form.price.data
        product.description = form.description.data
        product.quantity = form.quantity.data
        product.condition = form.condition.data
        product.status = form.status.data

        if form.picture.data:
            # Deleta imagem antiga do produto
            delete_picture(product.image_file, 'product_pics')

            # Salva nova imagem do produto
            product_image_file = save_picture(form.picture.data, 'product_pics', (1080, 1080))
            product.image_file = product_image_file

        repo.update_product(product)
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('products.product', product_id=product.id))

    elif request.method == 'GET':
        # Inicializa o formulário com os dados atuais
        form.title.data = product.name
        form.price.data = product.price
        form.description.data = product.description
        form.quantity.data = product.quantity
        form.condition.data = product.condition
        form.status.data = product.status
    
    return render_template('create_product.html', title='Atualizar Produto', form=form, legend='Atualizar Produto')

@products.route('/products/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    repo = ProductRepository(db)
    product = repo.get_product_by_id(product_id)

    if product.author != current_user:
        abort(403)

    repo.delete_product(product)
    flash('Produto deletado com sucesso!', 'success')
    return redirect(url_for('main.home'))