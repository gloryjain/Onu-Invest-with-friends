#Function to create an account from the bot

import requests
import json
import random

def createAccount(customerId, customer):
    customerId = customerId
    customer = customer
    #Glorys API key
    apiKey = '89e1407d751d9033c3bf258c76a33e79'
    accountType = 'Checking'

    url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)

    #Setting up account number at random 16-digit format
    accountNumber = str(random.randint(1000000000000000, 9999999999999999))

    payload = {
        "type": accountType,
        "nickname": customer + "'s Checking Account",
        "rewards": 1000,
        "balance": 5000,
        "account_number": accountNumber
        }

    response = requests.post( 
        url, 
        data=json.dumps(payload),
        headers={'content-type':'application/json'},
        )

    if response.status_code == 201:
        print('account created for', customer)

    return response.status_code == 201

def main():
    customerId = raw_input("To create an account, please enter a customer ID: ")
    customerName = raw_input("What is the customer's name?: ")
    if createAccount(customerId, customerName):
        print('Account creation for', customer, 'was successful')
    else:
        print('Error creating account, please try again')
    

main()
