#Function to create a new customer from the bot

import requests
import json

def createCustomer(first, last, stNum, stName, city, state, zip):
    apiKey = '508de63e607d501fc1617f4e39315b86' #kims api key

    url = "http://api.reimaginebanking.com/customers?key={}".format(apiKey)

    payload = {"first_name": first,
        "last_name":last,
        "address": {
            "street_number":stNum,
            "street_name": stName,
            "city": city,
            "state": state,
            "zip": zip
            }
        }
    response = requests.post(
        url, 
        data=json.dumps(payload), 
        headers={'content-type':'application/json'},
        )

    if response.status_code == 201:
        print('account created for', first)

    print(response.text)

first = 'Ben'
last = 'Stobaugh'
stNum = '500'
stName = 'Felisa Rincon'
city = 'San Juan'
state = 'PR'
zip = '00926'
#createCustomer(first, last, stNum, stName, city, state, zip)
