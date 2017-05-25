import requests
import datetime
import json

def withdrawCentral(total):

	url = "http://api.reimaginebanking.com/accounts/59271490ceb8abe24250de2f/withdrawals"
	querystring = {"key":"89e1407d751d9033c3bf258c76a33e79"}
	payload = json.dumps({"medium":"balance", "transaction_date":str(datetime.date.today()), "amount":total, "transaction_date":str(datetime.date.today()), "description": "buying the stock!!"})

	headers = {
    	'content-type': "application/json",
    	'cache-control': "no-cache",
    }

	response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
	print(response.text)

withdrawCentral(500)