#Function to create an account from the bot

import requests
import json
import random

def createAccount(customerId, customer):
    customerId = '5925e707a73e4942cdafd635'
    customer = 'Deondre'
    apiKey = '508de63e607d501fc1617f4e39315b86'
    accountType = 'Checking'

    url = 'http://api.reimaginebanking.com/customers/{}/accounts?key={}'.format(customerId,apiKey)

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
