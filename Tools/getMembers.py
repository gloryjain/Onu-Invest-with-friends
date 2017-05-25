#Function that gets groupme group members

import requests
import json

def getMembers():
    token = 'd98e567023a601356f8c53d177af4f91'
    groupId = '31349787'

    url = 'https://api.groupme.com/v3/groups/{}?token={}'.format(groupId,token)
    response = requests.get(url,)
    
    list_response = dict(response.json())
    list_response = list_response['response']
    #print list_response['members']
    members = []
    
    list_response = list_response['members']

    for i in range(0, len(list_response)):
       person = (list_response[i]['nickname']).split()[0]
       #print person
       members.append(str(person))

    return members
