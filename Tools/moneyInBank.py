#Function to get account balance

import requests
import json
import random

def getBalance():
    customerId = '5925e707a73e4942cdafd635'
    #Glorys API key
    apiKey = '89e1407d751d9033c3bf258c76a33e79'
    apiKey = '508de63e607d501fc1617f4e39315b86' #kims
    
    url = 'http://api.reimaginebanking.com/accounts?type=Checking&key={}'.format(apiKey)

    response = requests.get(
        url,
        )

    list_response = list(response.json())
    
    for i in range(0,len(list_response)):
        information_dic = list_response[i]
        print information_dic.keys()
        if information_dic['customer_id'] == int(customerId):
            print 


getBalance()
