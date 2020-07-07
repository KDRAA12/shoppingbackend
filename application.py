import os

from flask import Flask, session,jsonify,request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://lyqruykbdodlvv:f8b236c1caa1b44eff7d34380569791c1ff03647c6cb6667061fe19e67cc59c4@ec2-52-201-55-4.compute-1.amazonaws.com:5432/dd6te3jft2ujrt"

db=SQLAlchemy(app)


# Set up database



@app.route("/getProducts")
def get_all_product():
    products=Product.query.all()
    
    return jsonify({'products':[p.serialize() for p in products ]})

@app.route("/getProducts/<int:productId>")
def product(productId):

    p=Product.query.get(productId)
    if p:
        return jsonify({'success':True,'product':p.serialize()})
    else:
        return jsonify({'success':False})
@app.route("/addProduct",methods=['POST','GET'])
def add_product():
    name=request.form.get('name')
    price=request.form.get('price')
    description=request.form.get('description')

    p=Product(name=name,price=price,description=description)
    db.session.add(p)
    db.session.commit()
    
    return jsonify({'success':True})

@app.route("/deleteProduct/<int:productId>")
def delete(productId):
    p=Product.query.get(productId)
    if(p):
        buffer=True
        db.session.delete(p)
        db.session.commit()
    else:
        buffer=False
    return jsonify({'success':buffer})

@app.route("/updateProduct")
def updateProduct():
    productId=request.form.get('productId')
    p=Product.query.get(productId)
     
    if(p):
        buffer=True
            
        name=request.form.get('name')
        price=request.form.get('price')
        description=request.form.get('description')

        p=Product(name=name,price=price,description=description)
        db.session.add(p)
        db.session.commit()
    else:
        buffer=False
    return jsonify({'success':buffer})
class Product(db.Model):
    __tablename__="products"
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(50))
    price=db.Column(db.Float)
    description=db.Column(db.Text)

    def serialize(self):
        return {
            'id':self.id,
            'name':self.name,
            'price':self.price,
            'description':self.description,

        }
if __name__ == "__main__":
      # Allows for command line interaction with Flask application
    with app.app_context():
        main()