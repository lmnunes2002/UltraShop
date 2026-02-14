import math
from flask import Blueprint, render_template, flash, redirect, request, url_for, abort
from flask_login import current_user, login_required
from flaskblog.infra.connection import db
from flaskblog.repositories import ProductRepository, CommentRepository
from flaskblog.models import Comment
from flaskblog.blueprints.comments.forms import CommentForm, UpdateCommentForm
from flaskblog.blueprints.comments.utils import get_pagination_list

comments = Blueprint('comments', __name__)

@comments.route('/product/<int:product_id>/comment', methods=['POST'])
@login_required
def comment_product(product_id):
    form = CommentForm()

    repo_product = ProductRepository(db)
    product_obj = repo_product.get_product_by_id(product_id)

    if not product_obj:
        abort(404)

    if form.validate_on_submit():
        comment = Comment(
            content = form.content.data,
            stars = form.stars.data,
            target = product_obj,
            author = current_user
        )

        repo = CommentRepository(db)
        repo.add_comment(comment)
        flash('Comentário adicionado com sucesso!', 'success')
    else:
        flash('Erro ao adicionar comentário. Verifique os campos.', 'danger')
    return redirect(url_for('products.product', product_id=product_id))

@comments.route('/product/<int:comment_id>/update_comment', methods=['GET', 'POST'])
@login_required
def update_comment(comment_id):
    # Configuração comentários por página.
    PER_PAGE = 4
    page = request.args.get('page', 1, type=int)

    # Quantidade de itens à pular antes de paginar.
    offset = (page - 1) * PER_PAGE

    form = UpdateCommentForm()

    repo_comment = CommentRepository(db)

    comment = repo_comment.get_comment_by_id(comment_id)

    if comment.author != current_user:
        abort(403)
    
    repo_product = ProductRepository(db)
    product_id = comment.product_id
    product = repo_product.get_product_by_id(product_id)

    if form.validate_on_submit():
        comment.content = form.content.data
        comment.stars = form.stars.data        
        repo_comment.update_comment(comment)
        flash('Comentário atualizado com sucesso!', 'success')
        return redirect(url_for('products.product', product_id=product_id))
    
    elif request.method == 'GET':
        form.content.data = comment.content
        form.stars.data = comment.stars

    comments_paginated = repo_comment.list_comments_by_product_id(product_id, limit=PER_PAGE, offset=offset)
    total_comments = repo_comment.count_comments_by_product_id(product_id)

    # Divisão arredondada para cima do total de páginas.
    total_pages = math.ceil(total_comments / PER_PAGE)

    # Lista de paginação.
    pagination_list = get_pagination_list(page, total_pages)
    
    return render_template(
        'product.html',
        title=product.name,
        product=product,
        comments=comments_paginated,
        form=form,
        page=page,
        total_pages=total_pages,
        pagination_list=pagination_list
    )

@comments.route('/product/<int:comment_id>/delete_comment', methods=['POST'])
@login_required
def delete_comment(comment_id):
    repo_comment = CommentRepository(db)
    comment = repo_comment.get_comment_by_id(comment_id)

    if comment.author != current_user:
        abort(403)

    product_id = comment.product_id
    repo_comment.delete_comment(comment)
    flash('Comentário deletado com sucesso!', 'success')
    return redirect(url_for('products.product', product_id=product_id))