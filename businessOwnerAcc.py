from dotenv import load_dotenv
import os
import pymongo
load_dotenv()  # This line brings all environment variables from .env into os.environ
import connectModule as cM
from passlib.context import CryptContext
from pymongo import errors
import pandas as pd

#Handles mongo DB connection to accountInfo & businessInfo collection
userLoginCollection=cM.mongoConnect("accountInfo","userInformation")
businessInfoCollection=cM.mongoConnect("Businesses","businessInfo")

# Ensure businessID is unique
businessInfoCollection.create_index([("businessID", 1)], unique=True)

# Ensure the combination of businessName and zipCode is unique
businessInfoCollection.create_index([("businessName", 1), ("zipCode", 1)], unique=True)


#Prevents duplicate emails and username
userLoginCollection.create_index(["username","email"], unique=True)

#Encrypts passwords in database
pwd_encrypt= CryptContext(schemes=["bcrypt"], deprecated="auto")

def register_business(businessName,zipCode,ID,address,logoUrl):
    new_business = {
        "businessName": businessName,
        "zipCode": zipCode,
        "businessID": ID,
        "address": address,
        "logoUrl": logoUrl
    }

    try:
        result = businessInfoCollection.insert_one(new_business)
        print(f"Business registered with ID: {result.inserted_id}")
        return True
    except errors.DuplicateKeyError as e:
        print("Registration failed: Business ID or Name/Zip combination already exists.")
        return False


def register_business_owner(username, password, fullName, birthday, businessID):
    businessName = businessInfoCollection.find_one({"businessID": businessID},{"businessName":1,"_id":0})["businessName"]
    #password encryption object called
    hashed_password = pwd_encrypt.hash(password) 

    email=str(f"{username}@{businessName}.com")

    user_data = {

        "username": username,

        "email": email,

        "password": hashed_password,

        "fullName": fullName,

        "birthday": birthday,

        "businessId":businessID,

        "accountType":"owner"

    }


    #Attempt to add new user to database
    try:

        result = userLoginCollection.insert_one(user_data)

        return {"message": "Employee registered successfully", "user_id": str(result.inserted_id)}

    except pymongo.errors.DuplicateKeyError:

        return {"error": "Username or email already exists"}
    
def get_business_zip(businessID):

    business = businessInfoCollection.find_one(
        {"businessID": businessID},
        {"_id": 0, "zipCode": 1}
    )
    if business and "zipCode" in business:
        return business["zipCode"]
    return None

# Function to calculate tax
def taxCalculation(zipCode):
    df = pd.read_csv('Tax/taxes.csv')
    try:
        return df.loc[df['ZipCode'] == int(zipCode), 'EstimatedCombinedRate'].values[0]
    except IndexError:
        print("Invalid Zipcode! Using default value.")
        return 0.07


def register_employee(username, password, fullName, birthday, businessID):
    businessName = businessInfoCollection.find_one({"businessID": businessID},{"businessName":1,"_id":0})["businessName"]
    
    #password encryption object called
    hashed_password = pwd_encrypt.hash(password) 

    email=str(f"{username}@{businessName}.com")

    user_data = {

        "username": username,

        "email": email,

        "password": hashed_password,

        "fullName": fullName,

        "birthday": birthday,

        "businessID":businessID,

        "accountType":"employee"

    }


    #Attempt to add new user to database
    try:

        result = userLoginCollection.insert_one(user_data)

        return {"message": "Employee registered successfully", "user_id": str(result.inserted_id)}

    except pymongo.errors.DuplicateKeyError:

        return {"error": "Username or email already exists"}
