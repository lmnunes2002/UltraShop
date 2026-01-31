from flask import Blueprint, render_template, flash, redirect, request, url_for, abort
from flask_login import current_user, login_required
from flaskblog.infra.connection import db
from flaskblog.repositories import ProductRepository
from flaskblog.models import Product
from flaskblog.products.forms import ProductForm
from flaskblog.products.utils import save_picture

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
    repo = ProductRepository(db)
    product = repo.get_product_by_id(product_id)

    if product is None:
        abort(404)

    return render_template('product.html', title=product.name, product=product)

@products.route('/products/<int:product_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(product_id):
    repo = ProductRepository(db)
    product = repo.get_product_by_id(product_id)

    if product.author != current_user:
        abort(403)

    form = ProductForm()
    if form.validate_on_submit():
        product.name = form.title.data
        product.price = form.price.data
        product.description = form.description.data

        if form.picture.data:
            product_image_file = save_picture(form.picture.data, 'product_pics', (1080, 1080))
            product.image_file = product_image_file
        elif request.method == 'GET':
            form.title.data = product.name
            form.price.data = product.price
            form.description.data = product.description

        repo.update_product(product)
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('products.product', product_id=product.id))
    
    form.title.data = product.name
    form.price.data = product.price
    form.description.data = product.description
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
    PER_PAGE = 8
    page = request.args.get('page', 1, type=int)

    repo = UserRepository(db)
    user = repo.get_user_by_username(username)

    if user is None:
        abort(404)
        
    offset = (page - 1) * PER_PAGE

    repo = ProductRepository(db)
    products = repo.get_products_by_user_id(user.id, limit=PER_PAGE, offset=offset)
    total_products = repo.count_products_by_user_id(user.id)

    total_pages = math.ceil(total_products / PER_PAGE)

    pagination_list = get_pagination_list(page, total_pages)

    return render_template(
        'user_products.html',
        user=user,
        products=products,
        page=page,
        total_pages=total_pages,
        pagination_list=pagination_list,
        total_products=total_products
    )