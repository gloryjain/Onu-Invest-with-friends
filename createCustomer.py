import requests

url = "http://api.reimaginebanking.com/customers"

querystring = {"key":"89e1407d751d9033c3bf258c76a33e79"}

payload = "{\n  \"first_name\": \"Kim\",\n  \"last_name\": \"Santiago\",\n  \"address\": {\n    \"street_number\": \"1234\",\n    \"street_name\": \"Coder Ave\",\n    \"city\": \"Cupertino\",\n    \"state\": \"CA\",\n    \"zip\": \"22434\"\n  }\n}"
headers = {
    'key': "89e1407d751d9033c3bf258c76a33e79",
    'content-type': "application/json",
    'cache-control': "no-cache",
    'postman-token': "d1b4fe0e-5014-953e-0914-3f0c19d3d557"
    }

response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

print(response.text)