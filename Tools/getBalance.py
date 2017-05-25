#Function to get account balance

import requests
import json
import random

def getBalance(customerId):
    #Glorys API key
    apiKey = '89e1407d751d9033c3bf258c76a33e79'
    #apiKey = '508de63e607d501fc1617f4e39315b86' #kims
    #apiKey = '89e1407d751d9033c3bf258c76a33e79'

    url = 'http://api.reimaginebanking.com/accounts?type=Checking&key={}'.format(apiKey)

    response = requests.get(url,)

    list_response = list(response.json())
    
    for i in range(0,len(list_response)):
        information_dic = list_response[i]
        #print 'Nickname: ',information_dic['nickname'],'Account ID:', information_dic['_id'], 'Customer Id:',information_dic['customer_id']
        if information_dic['customer_id'] == customerId:
            return information_dic['balance']

