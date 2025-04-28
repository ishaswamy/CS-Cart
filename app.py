from uuid import uuid4
from flask import Flask, request, jsonify, session
from flask_cors import CORS
import shoppingCart as sc  
import menuChange as menu
from customerAcc import register_user, login_user, get_accountType
import os
from dotenv import load_dotenv
import orderStatus as status
from businessOwnerAcc import register_business_owner, register_employee, taxCalculation, get_business_zip

load_dotenv()

app = Flask(__name__) 


app.secret_key = os.getenv("secret_key")
app.config["SESSION_COOKIE_HTTPONLY"] = False  # Allow JS access if needed
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # Needed for cross-origin requests
app.config["SESSION_COOKIE_SECURE"] = False  # Set to True in production with HTTPS

CORS(app, supports_credentials=True)  # Allow session cookies

#Hardcoded businessID. Changing this changes what business is currently being accessed.
BUSINESSID="3"

#Returns current businessID for use in python scripts.
def getBusinessID():
    return str(BUSINESSID)

def checkAccountType(user=None):
    if "user" in session:
        account_type = get_accountType(session["user"])  # <- use session user
        return str(account_type)
    elif user:
        return get_accountType(user)
    else:
        return jsonify({"accountType": None}), 200


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
    zip_code = get_business_zip(getBusinessID())
    print(zip_code)
    if not zip_code:
        return jsonify({"error": "Zip code is required"}), 400
    tax_rate = taxCalculation(zip_code)
    return jsonify({"taxRate": tax_rate})

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

@app.route('/business-id', methods=['GET'])
def business_id():
    
    return jsonify({"businessID": getBusinessID()}), 200
    
@app.route('/get-businesses', methods=['GET'])
def get_businesses():
    from connectModule import mongoConnect
    business_col = mongoConnect("Businesses", "businessInfo")
    # pull only the ID and name
    docs = list(business_col.find({}, {"_id":0, "businessID":1, "businessName":1}))
    return jsonify({"businesses": docs}), 200

# API route to fetch all menu items for a business
@app.route("/get-menu", methods=["GET"])
def get_menu():

    try:
        menu_items = menu.get_menu_items(BUSINESSID)  
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


@app.route('/get-item')
def get_item():
    item_id = request.args.get("itemID")        # UUID string
    if not item_id:
        return jsonify({"message": "Missing itemID"}), 400

    item = menu.get_item(item_id)               # query by string key
    if not item:
        return jsonify({"message": "Item not found"}), 404
    item.pop("_id", None)
    return jsonify(item), 200


@app.route('/update-item', methods=['POST'])
def update_item():
    #Permissions check to prevent unauthorized access
    if checkAccountType()!="owner":
        return jsonify({"Invalid credentials"})
    data = request.json
    item_id = data.get("itemID")              
    if not item_id:
        return jsonify({"message": "Missing itemID"}), 400

    update_fields = data.get("update_fields", {})
    if not update_fields:
        return jsonify({"message": "No fields provided"}), 400

    result = menu.updateItem(item_id, update_fields)  
    return jsonify(result), 200




# API route to add an item to the cart
@app.route("/add-to-cart", methods=["POST"])
def add_to_cart():
    if checkAccountType()=="customer":
        data = request.json
        username = data.get("username")
        product = data.get("product")
        businessID = BUSINESSID
        product["businessID"] = businessID 
        if not username or not product:
            return jsonify({"error": "Username and product data are required"}), 400

        try:
            result = sc.add_to_cart(product, username)  # Add the item to the cart
            return jsonify(result), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    else:
        return ({"error":"Non-Customer cannot add items to"})

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
def checkout_route():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    try:
        result = sc.checkout(username)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# User registration route
@app.route("/signup", methods=["POST", "OPTIONS"])
def register():
    # Check if there's already a user logged in
    if "user" in session:
        return jsonify({"error": "User is already logged in"}), 400  # Early return if user is logged in
    
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

    # Check if there's already a user logged in
    if "user" in session:
        return jsonify({"error": "User is already logged in"}), 400  # Early return if user is logged in
    
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

@app.route("/accountType", methods=["GET"])
def accountType():
    if "user" in session:
        account_type = get_accountType(session["user"])  # <- use session user
        return jsonify({"accountType": account_type}), 200
    else:
        return jsonify({"accountType": None}), 200
    
@app.route("/get-order-status", methods=["GET"])
def get_order_status():
    try:
        orders = status.get_all_orders()  # Get all orders from the database
        return jsonify({"orders": orders}), 200  
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/update-item-status", methods=["POST"])
def update_item_status():
    #Permissions check to prevent unauthorized access
    if checkAccountType()!= "owner" and checkAccountType()!="employee":
        return jsonify({"error": "Invalid credentials"})
    data = request.json
    itemID   = data["itemID"]
    newStatus = data["itemStatus"]
    if newStatus == "completed":
        result = status.markItemCompleted(itemID)
    elif newStatus == "in_progress":
        result = status.markItemInProgress(itemID)
    elif newStatus == "incomplete":
        result = status.markItemIncomplete(itemID)
    else:
        return jsonify({"error": "Invalid status"}), 400

    return jsonify(result), 200

#API Call that clears orders from Order Page
@app.route("/clear-order", methods=["POST"])
def clear_order():
    #Permissions check to prevent unauthorized access
    if checkAccountType()!= "owner" and checkAccountType()!="employee":
        return jsonify({"error": "Invalid credentials"})
    try:
        data = request.json
        orderID = data.get("orderID")
        if not orderID:
            return jsonify({"error": "Missing orderID"}), 400

        result = status.clearOrder(orderID)
        if "message" in result:
            return jsonify(result), 200
        else:
            return jsonify({"error": result.get("error","Unknown error")}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/register_employee', methods=['POST'])
def register_employee_route():
    #Permissions check to prevent unauthorized access
    if checkAccountType() !="owner":
        return jsonify({"error": "Invalid credentials"})
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


#APP route to update shopping cart item
@app.route('/update-cart-item', methods=['POST'])
def update_cart_item_route():
    data = request.json
    username = data.get("username")
    itemID = data.get("itemID")
    updateFields = data.get("updateFields", {})

    response = sc.update_cart_item(username, itemID, updateFields)
    return jsonify(response)

#Gets address to show on Header
@app.route('/getBusinessHeaderInformation',methods=['GET'])
def getBusinessHeaderInformation():
    from connectModule import mongoConnect
    businessInfo=mongoConnect("Businesses","businessInfo")
    #Queries mongodb for the address and zipcode
    businessHeaderDisplay=businessInfo.find_one({"businessID":getBusinessID()},
                                  {"_id":0,"address":1,"zipCode":1,"businessLogoURL":1,"businessName":1})
    if businessHeaderDisplay:
        response = {
            "address": f"{businessHeaderDisplay['address']}, {businessHeaderDisplay['zipCode']}",
            "logoURL": businessHeaderDisplay["businessLogoURL"],
            "businessName": businessHeaderDisplay["businessName"]
        }
        return jsonify(response), 200
    else:
        return jsonify({"error": "Business not found"}), 404
    
#App route that adds items to menu
@app.route('/add-item', methods=['POST'])
def add_item_route():
    #Permissions check to prevent unauthorized access
    if checkAccountType() !="owner":
        return jsonify({"error": "Invalid credentials"})
    data = request.get_json()
    update_fields = data.get("update_fields")
    

    update_fields["businessID"] = BUSINESSID
    update_fields["itemID"] =  str(uuid4())

    if not update_fields["businessID"]:
        return jsonify({"message": "Business ID not found"}), 400

    result = menu.addItem(update_fields)
    return jsonify(result)

@app.route('/get-categories', methods=['GET'])
def get_categories_route():
    businessID = getBusinessID() 
    response = menu.get_categories(businessID)
    return jsonify({"categories": response})


@app.route('/add-category', methods=['POST'])
def add_category():
    #Permissions check to prevent unauthorized access
    if checkAccountType() !="owner":
        return jsonify({"error": "Invalid credentials"})
    data = request.get_json()
    category = data.get("category")
    categoryImageURL = data.get("categoryImageURL")
    businessID = getBusinessID()
    if not businessID or not category or not categoryImageURL:
        return jsonify({"error": "Missing required fields"}), 400

    result = menu.addCategory(category, businessID, categoryImageURL)  
    return jsonify(result), 201

@app.route('/delete-category', methods=['POST'])
def delete_category():
    #Permissions check to prevent unauthorized access
    if checkAccountType() !="owner":
        return jsonify({"error": "Invalid credentials"})
    data = request.get_json()
    category = data.get("category")
    businessID = getBusinessID()

    if not category:
        return jsonify({"error": "Missing category name"}), 400

    result = menu.deleteCategory(category, businessID)
    if "error" in result:
        return jsonify(result), 404
    return jsonify(result), 200

@app.route('/delete-menu-item', methods=['POST'])
def delete_menu_item():
    #Permissions check to prevent unauthorized access
    if checkAccountType() !="owner":
        return jsonify({"error": "Invalid credentials"})
    data = request.get_json()
    itemName = data.get("itemName")
    if not itemName:
        return jsonify({"error": "Missing itemName"}), 400

    businessID = getBusinessID()
    result = menu.deleteItem(itemName, businessID)
    status = 200 if "message" in result else 404
    return jsonify(result), status


if __name__ == "__main__":
    app.run(debug=True)  