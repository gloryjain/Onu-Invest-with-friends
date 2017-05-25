#Function to transfer funds from personal accounts to Pool Account

import requests
import json
from getBalance import getBalance
from getMembers import getMembers

# This function will take in the amount of money to be transferred to the
# Pool Account
def transferFunds(amount):
    #Get current people in group
    members = getMembers()
    print members

transferFunds(50)
