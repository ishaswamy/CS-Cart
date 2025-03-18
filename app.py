from flask import Flask, request, jsonify
from flask_cors import CORS
from customerAcc import register_user, login_user  
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)
CORS(app)  

# Function to calculate tax
def taxCalculation(zipCode):
    df = pd.read_csv('/home/codespace/CS-Cart/Tax/taxes.csv')
    return df.loc[df['ZipCode'] == zipCode, 'EstimatedCombinedRate'].values[0]

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
        return jsonify(result), 400  # Bad request if there's an error
    else:
        return jsonify(result), 201  # User created successfully

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username_or_email = data.get("username_or_email")
    password = data.get("password")

    result = login_user(username_or_email, password)

    if "error" in result:
        return jsonify(result), 400  # Bad request if credentials are wrong
    else:
        return jsonify(result), 200  # Success

if __name__ == "__main__":
    app.run(debug=True)

