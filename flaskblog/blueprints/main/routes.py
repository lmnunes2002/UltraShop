import math
from flask import Blueprint, render_template, request
from flaskblog.infra.connection import db
from flaskblog.repositories import ProductRepository
from flaskblog.blueprints.main.utils import get_pagination_list

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/home')
def home():
    # Configura produtos por página.
    PER_PAGE = 8
    page = request.args.get('page', 1, type=int)

    # Quantidade de itens à pular antes de paginar.
    offset = (page - 1) * PER_PAGE

    # Query de produtos.
    repo = ProductRepository(db)
    products = repo.list_products(limit=PER_PAGE, offset=offset)
    total_products = repo.count_products()

    # Divisão arredondada para cima do total de páginas.
    total_pages = math.ceil(total_products / PER_PAGE)

    # Lista de paginação.
    pagination_list = get_pagination_list(page, total_pages)

    return render_template(
        'home.html',
        products=products,
        page=page,
        total_pages=total_pages,
        pagination_list=pagination_list
    )

@main.route('/about')
def about():
    return render_template('about.html', title='Sobre nós')