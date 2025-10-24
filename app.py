# Importação
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy


# Instância do app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'

# Instância do banco de dados
db = SQLAlchemy(app)

# Definir modelo de produto
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)

# Criar o banco de dados
@app.route('/api/products/add', methods=['POST'])
def add_product():
    data = request.json
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"erro": "Dados inválidos"}), 400
    
    product = Product(
        name=data['name'],
        price=data['price'],
        description=data.get('description', '')
    )
    db.session.add(product)
    db.session.commit()
    return jsonify({"message": "produto cadastrado com sucesso"}), 201


# Rota para deletar um produto
@app.route('/api/products/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if  product:
       db.session.delete(product)
       db.session.commit()
       return jsonify({"message": "Produto deletetado com sucesso"})
    return jsonify({"ERROR": "Produto não encontrado"}), 404
    
    
# Definir rota raiz e a função
@app.route('/')
def hello_world():
    return 'Hello, world!'


# Executar o app
if __name__ == "__main__":
    app.run(debug=True)

