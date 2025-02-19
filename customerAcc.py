from dotenv import load_dotenv
import os
import pymongo
from passlib.context import CryptContext

load_dotenv()  # This line brings all environment variables from .env into os.environ

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
# Create a new client and connect to the server
client = MongoClient(os.getenv("CONNECTION_STRING"), server_api=ServerApi('1'))
accountInfoDatabase= client[os.getenv("USER_INFO_DATABASE")]
userLoginCollection= accountInfoDatabase[os.getenv("LOGIN_INFO_COL")]


#Prevents duplicate emails and username
userLoginCollection.create_index(["username","email"], unique=True)

pwd_encrypt= CryptContext(schemes=["bcrypt"], deprecated="auto")
def register_user(username, email, password):

    hashed_password = pwd_encrypt.hash(password) 



    user_data = {

        "username": username,

        "email": email,

        "password": hashed_password,

        "businessId":1

    }



    try:

        result = userLoginCollection.insert_one(user_data)

        return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

    except pymongo.errors.DuplicateKeyError:

        return {"error": "Username or email already exists"}
    
def login_user(username_or_email,password):
     # Find the user by username or email
    user = userLoginCollection.find_one({"$or": [{"username": username_or_email}, {"email": username_or_email}]})
    if user:
        if pwd_encrypt.verify(password, user["password"]):
                return {"message": "Login successful", "user_id": str(user["username"])}
        else:
                return {"error": "Incorrect Username or Password"}
    else:
        return {"error": "Incorrect Username or Password"}
