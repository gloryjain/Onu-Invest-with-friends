import requests
import json

j = []


with open("NASDAQ.txt") as f:
    for stock in f:


        a = stock.strip("\n").replace("[", "").replace("]", "").split("\t")
        ticker = a[0]
        name = a[1]
        nice_name = name.replace(" Inc", "").replace(" Ltd", "").replace(".", "")

        tmp = {"value":ticker, "synonyms":[ticker, name]}
        j.append(tmp)
        print('"'+ticker+'", "'+ticker+'", "'+name+'", "'+nice_name+'"')


#print(json.dumps(j))