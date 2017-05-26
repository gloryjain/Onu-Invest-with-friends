import requests

def getBalance(customerId):
    # Glorys API key
    apiKey = '89e1407d751d9033c3bf258c76a33e79'
    # apiKey = '508de63e607d501fc1617f4e39315b86' #kims
    # apiKey = '89e1407d751d9033c3bf258c76a33e79'

    url = 'http://api.reimaginebanking.com/accounts?type=Checking&key={}'.format(apiKey)

    response = requests.get(url, )

    list_response = list(response.json())

    for i in range(0, len(list_response)):
        information_dic = list_response[i]
        # print 'Nickname: ',information_dic['nickname'],'Account ID:', information_dic['_id'], 'Customer Id:',information_dic['customer_id']
        if information_dic['customer_id'] == customerId:
            return information_dic['balance']

def getMembers():
    token = 'd98e567023a601356f8c53d177af4f91'
    groupId = '31349787'

    url = 'https://api.groupme.com/v3/groups/{}?token={}'.format(groupId, token)
    response = requests.get(url, )

    list_response = dict(response.json())
    list_response = list_response['response']
    # print list_response['members']
    members = []

    list_response = list_response['members']

    for i in range(0, len(list_response)):
        person = (list_response[i]['nickname']).split()[0]
        # print person
        members.append(str(person))

    return members
