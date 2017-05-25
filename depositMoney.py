#Function to withraw money from the individual's bank
#and then deposit in the central Onu Bank
#will then subtract from the Onu bank
#Also keeps track how much 

import requests
import json
import random
import datetime

	
names = {"tester1":"5927271dceb8abe24250de57",
		"tester2":"59272734ceb8abe24250de58"}

def withdrawCentral(total):



def transfer(moneyTransferred,payerID, receiverID):	
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


# def getAccountID():
#     #Glorys API key                                                                                                                                                               
#     apiKey = '89e1407d751d9033c3bf258c76a33e79'
#     #apiKey = '508de63e607d501fc1617f4e39315b86' #kims                                                                                                                            
#     #apiKey = '89e1407d751d9033c3bf258c76a33e79'

#     url = 'http://api.reimaginebanking.com/accounts?type=Checking&key={}'.format(apiKey)

#     response = requests.get(url,)

#     list_response = list(response.json())

#     for i in range(0,len(list_response)):
#         information_dic = list_response[i]
#         print 'Nickname: ',information_dic['nickname'],'Account ID:', information_dic['_id'], 'Customer Id:',information_dic['customer_id']
#         #if information_dic['customer_id'] == customerId and information_dic['type'] == 'Checking':                                                                               
#         #    return information_dic['balance']                                                                                                                                    

# customerId = '5926f38da73e4942cdafd65b'
# print(getBalance(customerId))



# #print("Depositing everyone's money...")


# #glory = ("592713b4ceb8abe24250de24", "59271449ceb8abe24250de2a")
# #kobi = "592713c2ceb8abe24250de28", 
# #ben = "592713bfceb8abe24250de27"
# #kyle = "592713bcceb8abe24250de26" 
# #kim = "592713baceb8abe24250de25"

# #group = {"glory":glory,"kobi":kobi,"ben":ben, "kyle":kyle, "kim":kim}

# #users = [
# """	{'name': kobi
# 	 'group_me_id': 'dfkladslfkjdsa'
# 	 'capitalone_id': 'fdkflsaff'
# 	},
# 	{}
# 	]

# def groupAdd(name, customerID):
# 	group.update({name, customerID})

# def transfer(indivAmount):
# 	transferDate = datetime.date.today()

# 	for key, value in group.items():
# 		print key, "'s money is currently transferring to Onu..."
# 	print "Transfer complete"		
# withdrawIndiv()

# #def depositOnu(total):
# 	#print total
