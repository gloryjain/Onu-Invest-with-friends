"""
This bot listens to port 5002 for incoming connections from Facebook. It takes
in any messages that the bot receives and echos it back.
"""
from flask import Flask, request, render_template
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


verify = {}


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
        sendMessage("Confirmed 😊 Investing in "+names[ticker]+"!")
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
        transferFundsToPoolAccount(price)
        id = str(uuid1())
        verify[id] = {"ticker":ticker, "price":price}

        resp = requests.post(
            "https://api.mailgun.net/v3/send.helloben.co/messages",
            auth=("api", conf['mg_secret']),
            data={"from": "Onu <onu@send.helloben.co>",
                  "to": ["<Ben Stobuagh> legoben1998@gmail.com"],
                  "subject": "Please Confirm Transaction!",
                  "text": "Hi Ben!\n\n In order for your order for one share of "+names[ticker]+" ("+ticker+
                           ") to go through, please click on the link below. \n THIS WILL BUY THE SHARE FOR "+
                           locale.currency(price)+"!\n\n http://c1.ngrok.io/verify/"+id+" \n\nThanks!"})
        print(resp.text)




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

def transferFundsToPoolAccount(amount=0):
    sendMessage("Beginning Buy 😲 ... ")

    # Get current people in group
    groupMembers = getMembers()

    apiKey = '89e1407d751d9033c3bf258c76a33e79'
    receiver_id = '59271490ceb8abe24250de2f'

    url = 'http://api.reimaginebanking.com/customers?key={}'.format(apiKey)
    response = requests.get(url, )
    list_response2 = list(response.json())

    customer_ids = []
    account_ids = []

    for i in range(0, len(list_response2)):
        info = list_response2[i]
        first = info['first_name']
        customer_id = info['_id']
        if first in groupMembers:
            customer_ids.append(customer_id)
    # print customer_ids
    url = 'http://api.reimaginebanking.com/accounts?type=Checking&key={}'.format(apiKey)
    response = requests.get(url, )
    list_response = list(response.json())

    for i in range(0, len(list_response)):
        info = list_response[i]
        # print info
        customer_id = str(info['customer_id'])
        if customer_id in customer_ids:
            # print 'Found customer id in list'
            account_id = info['_id']
            account_ids.append(str(account_id))

    divideBy = len(account_ids)
    contributedAmount = amount / divideBy

    for i in range(0, len(account_ids)):
        time = str(date.today())
        url = 'http://api.reimaginebanking.com/accounts/{}/transfers?key={}'.format(account_ids[i], apiKey)
        payload = {
            'medium': 'balance',
            'payee_id': receiver_id,
            'amount': contributedAmount,
            'transaction_date': time,
            'description': 'Transferring ' + str(contributedAmount) + ' to Pool Account'
        }

        response = requests.post(
            url,
            data=json.dumps(payload),
            headers={'content-type': 'application/json'},
        )

    sendMessage("Successfully transferred funds into joint Capital One Account!  😄😄😄" )
    sendMessage("A confirmation email has been sent to the group owner. Clicking on the link will complete the transaction.")


def withdrawCentral(total):
    url = "http://api.reimaginebanking.com/accounts/59271490ceb8abe24250de2f/withdrawals"
    querystring = {"key": "89e1407d751d9033c3bf258c76a33e79"}
    payload = json.dumps({"medium": "balance", "transaction_date": str(date.today()), "amount": total,
                          "description": "buying the stock!!"})

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache",
    }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    print(response.text)



@app.route("/msg", methods=["GET", "POST"])
def groupme_message():
    print("hiya")
    j = request.json
    msg = j['text']
    group_size = 1


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
            ticker = ai['result']['parameters']['StockTickers']
            print("ticker", ticker)
            price = get_stock_price_friendly(ticker)
            print(price)
            sendMessage(price)

        if(event == "Buy Stock"):
            ticker = ai['result']['parameters']['StockTickers']

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

                msg = "%s was bought on %s for %s (%s each). It is now worth %s. (net %s)" % \
                      (s['ticker'], time, locale.currency(s['price']),
                       locale.currency(s['div_price']), locale.currency(price),
                       locale.currency(price - s['price'])
                       )
                sendMessage(msg)



            pass

        if(event == "StockGrade"):
            ticker = ai['result']['parameters']['StockTickers']
            grade = stock_grade(ticker)
            sendMessage('The grade of ' + ticker + ' is ' + grade)

        if(event == "Stock Info"):
            ticker = ai['result']['parameters']['StockTickers']

            endpoint = "https://api.cognitive.microsoft.com/bing/v5.0/news/search"
            headers = {"Ocp-Apim-Subscription-Key": conf['bing-search-key']}
            getvars = {"q": names[ticker], "mkt": "en-US"}

            req = requests.get(endpoint, headers=headers, params=getvars).text
            stories = json.loads(req)['value']
            print(stories)

            sendMessage("Here are some news stories about "+names[ticker] + " 😄")
            for story in stories[:4]:
                sendMessage(story['name'] + ": " + story['description'] +" - " + getShortURL(story['url']))

            pass
            url = "https://finance.yahoo.com/quote/" + ticker + "/?p=" + ticker
            sendMessage("Also see Yahoo Finance: " + url)

        #Command: help, tell me about yourself
        if(event == "Help Stock"):
            sendMessage("Onu help to the rescue!\nHi and welcome, I am Onu and I want to help you be a successful investor.\n " + \
                        "Some of the commands you could use are: \nOnu, what is the price of MSFT? \n" + \
                        "Onu, what are stocks? \n Onu, how can I invest? \n Onu, tell me more about APPL")
            sendMessage("Once you have started investing, I'll be able to tell you about your portfolio. Just use: \n Onu status or Onu portfolio")
            sendMessage("Go ahead, try it.")


        if(event == "Default Fallback Intent"):
            sendMessage("Sorry, I don't understand 😞")

        #How to invest
        if(event == "Help Invest"):
            sendMessage("It's actually very easy to start investing. Thank's to the technologies provided by Capital One Investments" + \
                        "I can help you invest in stocks that you and your friends can afford. If this is your first time" + \
                        "investing, fear no more! To start feel free to check this link out further: https://www.capitalone.com/financial-education/ for" + \
                        "more on understanding credit and basics or not! Just ask me about stock prices or even 'what is a stock?'. I can tryyyy and help.")

        #What is a stock
        if(event == "Account Balance"):
            bal = getBalance("592713e0ceb8abe24250de29")
            sendMessage("The current balance of the main account is "+ locale.currency(bal))



        if(event == "Info Stock"):
            url = getShortURL('https://content.capitaloneinvesting.com/mgdcon/knowledgecenter/Trade/Stocks/what_is_a_stock/what-is-a-stock.htm')
            sendMessage("Sooooo, yeah what is a stock? Let's ask Capital One! Check this out:" + url + " They're better at explaining than I am tbh...")

    else:
        pass




    return "okay"


@app.route("/verify/<uid>")
def verify_transaction(uid):
    sendMessage("Transaction has been verified! Buying one share of "+verify[uid]['ticker'])
    withdrawCentral(verify[uid]['price'])
    sendMessage("Congrats! You are collectively the new owner of one share of "+names[verify[uid]['ticker']] + "! 🤑")
    sendMessage("You can check the status of your investments by saying 'Onu status'")
    return "success"
    pass



@app.route("/admin/list")
def list_accts():
    accts = [
        {"name":"Glory Jain", "id":"592713b4ceb8abe24250de24"},
        {"name":"Kim Santiago", "id":"592713baceb8abe24250de25"},
        {"name":"Kyle Feng", "id":"592713bcceb8abe24250de26"},
        {"name":"Ben Stobaugh", "id":"592713bfceb8abe24250de27"},
        {"name":"Kobi Felton", "id":"592713c2ceb8abe24250de28"},
        {"name":"CENTRAL ACCT", "id":"592713e0ceb8abe24250de29"},
     ]

    str = ""

    for acct in accts:
        acct['bal'] = locale.currency(getBalance(acct['id']))

    return render_template("list.html", accts=accts)

@app.route("/send")
def send_page():
    if "msg" in request.args:
        print("sending ")
        sendMessage(request.args['msg'])

    return render_template("send.html" )


@app.route("/")
def home():
    return "<br><br><br><br><h1 style='text-align:center;'>O N U</h1>"



if __name__ == "__main__":
    print("msg", sendMessage("Hiya, it's Onu, your stock investing robot friend! Say 'onu help' to see what I can do!").text)
    app.run(port=5002, debug=True)
