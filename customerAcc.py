from dotenv import load_dotenv
import os
import pymongo
load_dotenv()  # This line brings all environment variables from .env into os.environ
import connectModule as cM
from passlib.context import CryptContext

#Handles mongo DB connection to accountInfo collection
userLoginCollection=cM.mongoConnect("accountInfo","userInformation")

#Prevents duplicate emails and username
userLoginCollection.create_index(["businessID", "username"], unique=True)
userLoginCollection.create_index(["businessID", "email"], unique=True)


#Encrypts passwords in database
pwd_encrypt= CryptContext(schemes=["bcrypt"], deprecated="auto")

def accountValidate(username):
    from app import getBusinessID
     # Find the user by username or email
    user = userLoginCollection.find_one({"username": username, "businessID": getBusinessID()})
    if user:
        return True
    else:
        return False

def register_user(username, email, password, fullName, birthday, businessID):

    #password encryption object called
    hashed_password = pwd_encrypt.hash(password) 



    user_data = {

        "username": username,

        "email": email,

        "password": hashed_password,

        "fullName": fullName,

        "birthday": birthday,

        "businessID":businessID,

        "accountType":"customer"

    }


    #Attempt to add new user to database
    try:

        result = userLoginCollection.insert_one(user_data)

        return {"message": "User registered successfully", "user_id": str(result.inserted_id)}

    except pymongo.errors.DuplicateKeyError:

        return {"error": "Username or email already exists"}
    
def login_user(username_or_email,password):
    from app import getBusinessID
     # Find the user by username or email
    user = userLoginCollection.find_one({"$or": [{"username": username_or_email}, {"email": username_or_email}],"businessID":getBusinessID()})
    if user:
        #Checks encrypted password
        if pwd_encrypt.verify(password, user["password"]):
                return {"message": "Login successful", "user_id": str(user["username"]),"accountType":str(user["accountType"])}
        else:
                return {"error": "Incorrect Username or Password"}
    else:
        return {"error": "Incorrect Username or Password"}
    
def get_accountType(username):
    from app import getBusinessID
    user= userLoginCollection.find_one({"username":username,"businessID":getBusinessID()})
    if user:
        return user["accountType"]
    else:
        return None

def change_password(username_or_email,oldPassword,newPassword):
     # Find the user by username or email
    user = userLoginCollection.find_one({"$or": [{"username": username_or_email}, {"email": username_or_email}]})
    if user:
        if pwd_encrypt.verify(oldPassword, user["password"]):
                user["password"]=newPassword
                return {"message": "Password Change Successful", "user_id": str(user["username"])}
        else:
                return {"error": "Incorrect Password"}
    else:
        return {"error": "Incorrect Password"}