#Function to withraw money from the individual's bank
#and then deposit in the central Onu Bank
#will then subtract from the Onu bank
#Also keeps track how much 

import requests
import json
import random
import datetime
from getBalance import getBalance
from getMembers import getMembers
	
names = {"tester1":"5927271dceb8abe24250de57",
       	"tester2":"59272734ceb8abe24250de58"}

def transferFunds(moneyTransferred,payerID, receiverID):	
	
	url = "http://api.reimaginebanking.com/accounts/"+payerID+"/transfers"
	querystring = {"key":"89e1407d751d9033c3bf258c76a33e79"}
#	payload = '{"medium": "balance", "payee_id": receiverID, "amount": '+moneyTransferred+' ,"transaction_date": '+str(datetime.date.today())+', "description": "transferring money"}'
	payload = json.dumps({"medium":"balance", "payee_id":receiverID, "amount":moneyTransferred, "transaction_date":str(datetime.date.today()), "description": "transferring money"})
	print payload
	headers = {
    	'content-type': "application/json",
    	'cache-control': "no-cache"
    	}

	response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
	print(response.text)

transfer(2000,names["tester2"],names["tester1"])
