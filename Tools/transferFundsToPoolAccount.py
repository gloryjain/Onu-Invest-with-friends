#Function to transfer funds from personal accounts to Pool Account

import datetime
import requests
import json
from getBalance import getBalance
from getMembers import getMembers

# This function will take in the amount of money to be transferred to the
# Pool Account
def transferFundsToPoolAccount(amount=0):
    #Get current people in group
    groupMembers = getMembers()
    
    apiKey = '89e1407d751d9033c3bf258c76a33e79'
    receiver_id = '59271490ceb8abe24250de2f'

    url = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)
    response = requests.get(url,)
    list_response2 = list(response.json())

    customer_ids = []
    account_ids = []
    
    for i in range(0, len(list_response2)):
        info = list_response2[i]
        first = info['first_name']
        customer_id = info['_id']
        if first in groupMembers:
            customer_ids.append(customer_id)
    #print customer_ids
    url = 'http://api.reimaginebanking.com/accounts?type=Checking&key={}'.format(apiKey)
    response = requests.get(url,)
    list_response = list(response.json())

    for i in range(0, len(list_response)):
        info = list_response[i]
        #print info
        customer_id = str(info['customer_id'])
        if customer_id in customer_ids:
            #print 'Found customer id in list'
            account_id = info['_id']
            account_ids.append(str(account_id))
    
    divideBy = len(account_ids)
    contributedAmount = amount / divideBy

    
    for i in range(0, len(account_ids)):
        time = str(datetime.date.today())
        url = 'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'.format(account_ids[i], apiKey)
        payload = {
            'medium':'balance',
            'payee_id':receiver_id,
            'amount': contributedAmount,
            'transaction_date': time,
            'description': 'Transferring '+str(contributedAmount)+' to Pool Account'
            }
        
        response = requests.post(
            url,
            data = json.dumps(payload),
            headers = {'content-type':'application/json'},
            )
        
        #if response.status_code == 201:
         #   print'Transfer of', contributedAmount,'from some random to pool account was successful'
        
#print response.text
