from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import pymongo
import pandas as pd
from dotenv import load_dotenv
from uuid import uuid4
import connectModule as cM
from customerAcc import register_user, login_user  

load_dotenv()  

app = Flask(__name__)
CORS(app)  

# Connect to MongoDB collections
cartCollection = cM.mongoConnect("accountInfo", "shoppingCart")
orderCollection = cM.mongoConnect("accountInfo", "orderStatus")

@app.route("/get-tax", methods=["GET"])
def get_tax():
    zip_code = request.args.get("zipCode", type=int)
    if not zip_code:
        return jsonify({"error": "Zip code is required"}), 400

    try:
        tax_rate = taxCalculation(zip_code)
        return jsonify({"taxRate": tax_rate})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
# Function to add items to the shopping cart
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    data = request.json
    if not data or "username" not in data or "product" not in data:
        return jsonify({"error": "Username and product data are required"}), 400

    product = data["product"]
    username = data["username"]
    
    # Generate unique item ID and associate with user
    product.update({"username": username, "itemID": str(uuid4())})

    cartCollection.insert_one(product)
    return jsonify({"message": "Item successfully added to cart"}), 201

# Function to checkout all cart items for a user
@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    if not data or "username" not in data:
        return jsonify({"error": "Username is required"}), 400

    username = data["username"]
    orderID = str(uuid4())
    orderList = list(cartCollection.find({"username": username}))

    if not orderList:
        return jsonify({"error": "Cart is empty"}), 400

    for order in orderList:
        order.update({"orderID": orderID, "orderStatus": "incomplete"})
        order.pop("_id", None)  # Remove MongoDB document ID to prevent duplicate key errors

    orderCollection.insert_many(orderList)
    cartCollection.delete_many({"username": username})

    return jsonify({"message": f"Checkout successful. Order #{orderID} has been created."}), 201

# User registration route
@app.route("/signup", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return "", 200 

    data = request.json  
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    fullName = data.get("name") 
    birthday = data.get("birthday")  
    businessID = data.get("restaurant")  

    result = register_user(username, email, password, fullName, birthday, businessID)

    if "error" in result:
        return jsonify(result), 400  
    return jsonify(result), 201  

# User login route
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username_or_email = data.get("username_or_email")
    password = data.get("password")

    result = login_user(username_or_email, password)

    if "error" in result:
        return jsonify(result), 400  
    return jsonify(result), 200  

if __name__ == "__main__":
    app.run(debug=True)
