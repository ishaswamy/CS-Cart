from flask import Flask, request, jsonify
from flask_cors import CORS
from customerAcc import register_user, login_user  
import os
from dotenv import load_dotenv

load_dotenv()  

app = Flask(__name__)
CORS(app)  

@app.route("/signup", methods=["POST", "OPTIONS"])
def register():
    if request.method == "OPTIONS":
        return "", 200 
    data = request.json  
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    businessID = data.get("businessID")

    result = register_user(username, email, password, businessID)

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
