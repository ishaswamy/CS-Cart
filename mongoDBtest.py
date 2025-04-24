from dotenv import load_dotenv
import os
load_dotenv()  # This line brings all environment variables from .env into os.environ

#import customer account login/signup
'''import menuChange as mChan
import orderStatus as orStat
import shoppingCart as sCart
from bson import ObjectId'''
from app import getBusinessID
from bson.objectid import ObjectId
from customerAcc import get_accountType
#import shoppingCart
#import orderStatus
from businessOwnerAcc import taxCalculation

print(taxCalculation(33063))

