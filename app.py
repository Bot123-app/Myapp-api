import os

from flask import Flask, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Database configuration (update these with your actual database credentials)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/myshop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
@app.route('/static/<filename>')

def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)
# Define the Product model
class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'))
    image = db.Column(db.String(255))

# Route to get all products
@app.route('/products', methods=['GET'])
def get_all_products():
    try:
        products = Product.query.all()
        result = [
            {
                'product_id': product.product_id,
                'title': product.title,
                'price': str(product.price),
                'description': product.description,
                'category_id': product.category_id,
                'image': product.image
            }
            for product in products
        ]
        return jsonify(result), 200
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

# Route to get a product by product_id
@app.route('/products/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    try:
        product = Product.query.get(product_id)
        if product:
            result = {
                'product_id': product.product_id,
                'title': product.title,
                'price': str(product.price),
                'description': product.description,
                'category_id': product.category_id,
                'image': product.image
            }
            return jsonify(result), 200
        else:
            return jsonify({"message": "Product not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
