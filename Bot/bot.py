"""
This bot listens to port 5002 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
from flask import Flask, request
from pymessenger.bot import Bot
import requests
import json
import string
import random
import quandl
import locale
from datetime import *
from uuid import uuid1

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.executors.pool import ThreadPoolExecutor

executors = {
    'default': ThreadPoolExecutor(30)
}
sc = BackgroundScheduler(executors=executors)
sc.start()



app = Flask(__name__)
conf = json.loads(open("config.json").read())

locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8')) # Set locale to en_US
quandl.ApiConfig.api_key = "V5uEXA4L1zfc9Q6Dp9Lz" # Set API key



def checkLikeAmount(msg_id, like_target, ticker, price, div_price, job_id):
    data = {"token": conf['GM_TOKEN'], "limit": "20", "after_id":msg_id}
    msgs = requests.get("https://api.groupme.com/v3/groups/" + conf['GM_GROUP'] + "/messages", params=data).json()

    print(msgs['response']['messages'][0])
    if(len(msgs['response']['messages'][0]['favorited_by']) >= like_target):
        sendMessage("Confirmed 😊 Investing in "+ticker+"!")
        sc.remove_job(job_id)
        #todo: do shit






# Returns price info in a pandas DataFrame
def get_stock_info(ticker, dataset, suffix, start_date='', end_date=''):
    return quandl.get(dataset + '/' + ticker.upper() + suffix, start_date=start_date, end_date=end_date)

# Returns end-of-day stock price from the previous day
def get_stock_price(ticker):
    # Wiki prices
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    try:
        data = get_stock_info(ticker, dataset='EOD', suffix='', start_date=yesterday)
    except quandl.errors.quandl_error.ForbiddenError:
        data = get_stock_info(ticker, dataset='WIKI', suffix='', start_date=yesterday)
    return data.tail(1)['Close'].tolist()[0]

def plot_stock_earnings(ticker):
    # Core US Fundamentals Data
    # Earnings per Basic Share (Most Recent - Quarterly)
    data = get_stock_info(ticker, dataset='SF1', suffix='_EPS_MRQ')
    # print data
    data.plot()
    # plot
    return data

# Returns stock price in a user-friendly way
# https://stackoverflow.com/questions/320929/currency-formatting-in-python
def get_stock_price_friendly(ticker):
    try:
        price = get_stock_price(ticker)
        price_pretty = locale.currency(price)
        return "Yesterday's end-of-day price for %s is %s." % (ticker.upper(), price_pretty)
    except quandl.errors.quandl_error.NotFoundError as e:
        # print e # debug
        return "Sorry, %s is not a valid ticker symbol name." % ticker


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
        print("omu here")
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

            group_size = 5
            price = get_stock_price(ticker)
            div_price = price / group_size

            msg = "The current price of %s is %s, split among each of %s members, each of you will have to pay %s " \
                  % (ticker.upper(), locale.currency(price), group_size,locale.currency(div_price))
            sendMessage(msg)
            sendMessage("Favorite THIS message to confirm!") #todo: me send?
            prev_msg_id = getMostRecentMSG()
            job_id = str(uuid1())
            sc.add_job(checkLikeAmount, 'interval', args=[prev_msg_id, group_size, ticker, price, div_price, job_id], seconds=10, id=job_id)
    else:
        pass




    return "okay"





if __name__ == "__main__":
    app.run(port=5002, debug=True)