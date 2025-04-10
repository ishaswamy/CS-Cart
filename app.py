from flask import Flask, request, jsonify, session
from flask_cors import CORS
import shoppingCart as sc  
import menuChange as menu
from customerAcc import register_user, login_user
import os
import pandas as pd
from dotenv import load_dotenv
import orderStatus as status
from businessOwnerAcc import register_business_owner, register_employee

load_dotenv()

app = Flask(__name__) 


app.secret_key = os.getenv("secret_key")
app.config["SESSION_COOKIE_HTTPONLY"] = False  # Allow JS access if needed
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Needed for cross-origin requests
app.config["SESSION_COOKIE_SECURE"] = False  # Set to True in production with HTTPS

CORS(app, supports_credentials=True)  # Allow session cookies

#Hardcoded businessID. Changing this changes what business is currently being accessed.
BUSINESSID=1

#Returns current businessID for use in python scripts.
def getBusinessID():
    return str(BUSINESSID)
# Function to calculate tax
def taxCalculation(zipCode):
    df = pd.read_csv('Tax/taxes.csv')
    return df.loc[df['ZipCode'] == zipCode, 'EstimatedCombinedRate'].values[0]

#Reads addons that are selected true for display under orders.
def readAddons(product):
    addonList=()
    for item, available in product['freeItems'].items():
        if available:
            addonList.append(item)
            
    #Grabs free toggle items
    for item in product['freeToggleItems']:
        if item.get('selected',True):
            addonList.append(item)

    #Grabs paid toggle items
    for item in product['paidToggleItems']:
        if item.get('selected',True):
            addonList.append(item)

    #Grabs paid items 
    for item in product['paidItems']:
        if item.get('selected',True):
            addonList.append(item)
    return addonList

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

# API route to fetch all cart items for a user
@app.route("/get-cart", methods=["GET"])
def get_cart():
    username = request.args.get("username", type=str)
    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        cart_items = sc.get_cart_items(username)  # Fetch the cart items from the database
        return jsonify({"cartItems": cart_items}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# API route to fetch all menu items for a business
@app.route("/get-menu", methods=["GET"])
def get_menu():
    username = request.args.get("username", type=str)
    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        menu_items = menu.get_menu_items(username)  
        return jsonify({"menuItems": menu_items}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/get-specific-items", methods=["GET"])
def get_specific_items():
    businessID=BUSINESSID
    category = request.args.get("category", type=str)
    if not businessID:
        return jsonify({"error": "Invalid BusinessID Configured"}), 400
    if not category:
        return jsonify({"error": "Category is required"}), 400

    try:
        menu_items = menu.get_specific_category_items(businessID,category)  
        
        return jsonify({"menuItems": menu_items}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get-item', methods=['GET'])
def get_item():
    try:
        item_id = int(request.args.get("itemID", 0))  
    except ValueError:
        return jsonify({"message": "Invalid itemID format"}), 400

    if not item_id:
        return jsonify({"message": "Missing itemID"}), 400

    item = menu.get_menu_items(item_id)

    if not item:
        return jsonify({"message": "Item not found"}), 404

    return jsonify(item), 200




# API route to add an item to the cart
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    data = request.json
    username = data.get("username")
    product = data.get("product")

    if not username or not product:
        return jsonify({"error": "Username and product data are required"}), 400

    try:
        result = sc.add_to_cart(product, username)  # Add the item to the cart
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route to delete an item from the cart
@app.route("/delete-item", methods=["POST"])
def delete_item():
    data = request.json
    username = data.get("username")
    itemID = data.get("itemID")

    if not username or not itemID:
        return jsonify({"error": "Username and itemID are required"}), 400

    try:
        result = sc.delete_item(username, itemID)  # Delete the item from the cart
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# API route to checkout the cart and create an order
@app.route("/checkout", methods=["POST"])
def checkout():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        result = sc.checkout(username)  # Checkout and create an order
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

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
        return jsonify(result), 400  # Bad request if there's an error
    else:
        return jsonify(result), 201  # User created successfully

# User login route
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username_or_email = data.get("username_or_email")
    password = data.get("password")

    result = login_user(username_or_email, password)

    if "error" in result:
        return jsonify(result), 400  # Bad request if credentials are wrong
    else:
        session["user"]=result["user_id"]
        return jsonify(result), 200  # Success
    
#User logout route
@app.route("/logout",methods=["POST"])
def logout():
    session.pop("user", None)  # Remove user session
    return {"message": "Logged out successfully"}

#Checks which user is logged in
@app.route("/account", methods=["GET"])
def account():
    if "user" in session:
        #print(f"Session user: {session['user']} is here")
        return {"message": f"User {session['user']} is logged in"},200
    print("User lookup failed.")
    return {"error": "No user logged in"},401



@app.route("/get-order-status", methods=["GET"])
def get_order_status():
    try:
        orders = status.get_all_orders()  # Get all orders from the database
        return jsonify({"orders": orders}), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update-order-status", methods=["POST"])
def update_order_status():
    try:
        # Extract data from the request
        data = request.json
        orderID = data["orderID"]
        newStatus = data["orderStatus"]

        # Directly handle the status update using the specific functions
        if newStatus == "completed":
            result = status.markOrderCompleted(orderID)
        elif newStatus == "incomplete":
            result = status.markOrderIncomplete(orderID)
        elif newStatus == "in_progress":
            result = status.markOrderInProgress(orderID)
        elif newStatus == "clear":
            result = status.clearOrder(orderID)  
        else:
            return jsonify({"error": "Invalid order status provided."}), 400

        return jsonify(result), 200 

    except Exception as e:
        return jsonify({"error": str(e)}), 500
@app.route('/register_employee', methods=['POST'])
def register_employee_route():
    data = request.json
    if not all(k in data for k in ["username", "password", "fullName", "birthday", "businessID"]):
        return jsonify({"error": "Missing required fields"}), 400

    result = register_employee(
        username=data["username"],
        password=data["password"],
        fullName=data["fullName"],
        birthday=data["birthday"],
        businessID=data["businessID"]
    )
    return jsonify(result), 200


@app.route('/update-item', methods=['POST'])
def update_item():
    data = request.json
    try:
        item_id = int(data.get("itemID", 0))  # Convert to int
    except ValueError:
        return jsonify({"message": "Invalid itemID format"}), 400

    if not item_id:
        return jsonify({"message": "Missing required field: itemID"}), 400

    update_fields = data.get("update_fields", {})
    if not update_fields:
        return jsonify({"message": "No fields provided for update."}), 400
    response = menu.updateItem(item_id, update_fields)
    return jsonify(response)


@app.route('/update-cart-item', methods=['POST'])
def update_cart_item_route():
    data = request.json
    username = data.get("username")
    itemID = data.get("itemID")
    updateFields = data.get("updateFields", {})

    response = sc.update_cart_item(username, itemID, updateFields)
    return jsonify(response)






if __name__ == "__main__":
    app.run(debug=True)  