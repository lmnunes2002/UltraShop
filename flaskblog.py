from flask import Flask, render_template
app = Flask(__name__)

products = [
    {
        'name': 'Laptop',
        'price': 999.99,
        'description': 'Um laptop de alto desempenho adequado para todas as suas necessidades de computação.',
        'author': 'Joãozinho',
        'date_posted': '20/08/2024'
    },
    {
        'name': 'Smartphone',
        'price': 499.99,
        'description': 'Um smartphone elegante com os recursos mais recentes e uma bela tela.',
        'author': 'Mariazinha',
        'date_posted': '15/09/2024'
    }
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html', title='Sobre nós')

@app.route('/login')
def login():
    return "Seja bem-vindo ao login"

@app.route('/register')
def register():
    return "Seja bem-vindo ao registro"

if __name__ == '__main__':
    app.run(debug=True)