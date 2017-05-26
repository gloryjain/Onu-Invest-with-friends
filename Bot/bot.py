"""
This bot listens to port 5002 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
from flask import Flask, request
import requests
import json
import string
import random
import quandl
import locale
from datetime import *
from uuid import uuid1
from dateutil.parser import parse

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor

from stock_price import *


executors = {
    'default': ThreadPoolExecutor(30)
}
sc = BackgroundScheduler(executors=executors)
sc.start()



app = Flask(__name__)
conf = json.loads(open("config.json").read())
names = json.loads(open("stocks.json").read())



locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8')) # Set locale to en_US
quandl.ApiConfig.api_key = "V5uEXA4L1zfc9Q6Dp9Lz" # Set API key


def getShortURL(url):
    print("getting bitly of", url)

    resp = requests.get("https://api-ssl.bitly.com/v3/shorten", params = {
        "domain":"bit.ly", "longUrl":url, "access_token":conf['bitly_token']
    })

    try:
        return resp.json()['data']['url']
    except Exception:
        return url

def checkLikeAmount(msg_id, like_target, ticker, price, div_price, job_id):
    data = {"token": conf['GM_TOKEN'], "limit": "20", "after_id":msg_id}
    msgs = requests.get("https://api.groupme.com/v3/groups/" + conf['GM_GROUP'] + "/messages", params=data).json()

    print(msgs['response']['messages'][0])
    if(len(msgs['response']['messages'][0]['favorited_by']) >= like_target):
        sendMessage("Confirmed 😊 Investing in "+ticker+"!")
        sc.remove_job(job_id)

        # Write stock info to file
        # (Sorry)
        tmp = {
            "ticker":ticker,
            "price":price,
            "div_price":div_price,
            "date":str(datetime.now())
        }

        cur = json.loads(open("db.json").read())
        cur.append(tmp)
        open("db.json", "w").write(json.dumps(cur))

        #todo: do shit



def sendMessage(msg, img=None):
    data = {
        "bot_id":conf["GM_BOT"],
        "text":msg
    }
    return requests.post("https://api.groupme.com/v3/bots/post", data=data)


def getSessID():  # Generates a random ID
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(36))


def getNLP(query):
    print(getSessID())
    headers = {"Authorization": "Bearer "+conf['APIAI_TOKEN']}
    url = "https://api.api.ai/v1/query"
    data = {"query":query, "lang":"en", "sessionId":getSessID()}
    print("sending req")
    return requests.get(url, headers=headers, params=data).json()


def getMostRecentMSG():
    data = {"token":conf['GM_TOKEN'], "limit":"20"}
    msgs =  requests.get("https://api.groupme.com/v3/groups/"+conf['GM_GROUP']+"/messages", params=data).json()
    print("msgs", msgs['response']['messages'])
    for i in range(len(msgs['response']['messages'])):
        m = msgs['response']['messages'][i]
        if(m['sender_type'] == 'bot'):
            return msgs['response']['messages'][i+1]["id"]



@app.route("/msg", methods=["GET", "POST"])
def groupme_message():
    print("hiya")
    j = request.json
    msg = j['text']

    if(j['sender_type'] == 'bot'):
        return "nope"

    if(msg.lower().find("onu") != -1):
        print("onu here")
        sendtxt = msg.replace(",", "").replace("onu", "") #todo: regex
        ai = getNLP(sendtxt)
        print(ai)

        #todo: error handling

        event = ai['result']['metadata']['intentName']

        if(event == "Price of stock"):
            ticker = ai['result']['parameters']['StockTickers'] #todo: no full full names
            print("ticker", ticker)
            price = get_stock_price_friendly(ticker)
            print(price)
            sendMessage(price)

        if(event == "Buy Stock"):
            ticker = ai['result']['parameters']['StockTickers']

            group_size = 1
            price = get_stock_price(ticker)
            div_price = price / group_size

            msg = "The current price of %s was %s, split among each of %s members, each of you will have to pay %s " \
                  % (ticker.upper(), locale.currency(price), group_size,locale.currency(div_price))
            sendMessage(msg)
            sendMessage("Favorite THIS message to confirm!") #todo: me send?
            prev_msg_id = getMostRecentMSG()
            job_id = str(uuid1())
            sc.add_job(checkLikeAmount, 'interval', args=[prev_msg_id, group_size, ticker, price, div_price, job_id], seconds=10, id=job_id)

        if(event == "Check Status"):
            stocks = json.loads(open("db.json").read())

            sendMessage("Your portfolio is as follows:")



            for s in stocks:
                time = parse(s['date']).strftime("%d/%m/%y at %I:%M%p")
                price = get_stock_price(s['ticker'])

                msg = "%s was bough on %s for %s (%s each). It is now worth %s. (net %s)" % \
                      (s['ticker'], time, locale.currency(s['price']),
                       locale.currency(s['div_price']), locale.currency(price),
                       locale.currency(price - s['price'])
                       )
                sendMessage(msg)



            pass

        if(event == "Stock Info"):
            ticker = ai['result']['parameters']['StockTickers']

            endpoint = "https://api.cognitive.microsoft.com/bing/v5.0/news/search"
            headers = {"Ocp-Apim-Subscription-Key": conf['bing-search-key']}
            getvars = {"q": names[ticker], "mkt": "en-US"}

            req = requests.get(endpoint, headers=headers, params=getvars).text
            stories = json.loads(req)['value']
            print(stories)

            sendMessage("Here are some news stories about "+names[ticker])
            for story in stories[:4]:
                sendMessage(story['name'] + ":\n >" + story['description'] +"\n more at" + getShortURL(story['url']))

            pass

        #Command: help, tell me about yourself
        if(event == "Help Stock"):
            sendMessage("Onu help to the rescue!\nHi and welcome, I am Onu and I want to help you be a successful investor.\n " + \
                        "Some of the commands you could use are: \n Onu, tell me about APPL \n Onu, tell me about MSFT \n" + \
                            "Onu, what are stocks? \n Onu, how can I invest? \n Onu, tell me more about APPL")
            sendMessage("Once you have started investing, I'll be able to tell you about your portfolio. Just use: \n Onu status or Onu portfolio")
            sendMessage("Go ahead, try it.")

        #How to invest
        if(event == "Help Invest"):
            url = getShortURL()
            sendMessage("It's actually very easy to start investing. Thank's to the technologies provided by Capital One Investments" + \
                        "I can help you invest in stocks that you and your friends can afford. If this is your first time" + \
                        "investing, fear no more! To start feel free to check this link out further: https://www.capitalone.com/financial-education/ for" + \
                        "more on understanding credit and basics or not! Just ask me about stock prices or even 'what is a stock?'. I can tryyyy and help.")

        #What is a stock
        if(event == "Info Stock"):
            url = getShortURL('https://content.capitaloneinvesting.com/mgdcon/knowledgecenter/Trade/Stocks/what_is_a_stock/what-is-a-stock.htm')
            sendMessage("Sooooo, yeah what is a stock? Let's ask Capital One! Check this out:" + url + " They're better at explaining than I am tbh...")

    else:
        pass




    return "okay"





if __name__ == "__main__":
    print("msg", sendMessage("Hiya, it's Onu, your stock investing robot friend! Say 'onu help' to see what I can do!").text)
    app.run(port=5002, debug=True)
