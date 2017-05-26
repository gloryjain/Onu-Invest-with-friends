# Onu: Make money with your Friends

# Why?

The earlier you start investing, the better.

However, millenials are investing [less than previous generations](http://www.businessinsider.com/why-so-few-millennials-invest-in-the-stock-market-2016-7).
So, the question is, how can we make it easier for students to invest?

Onu is a chatbot designed to help people start investing with friends, making it both fun and profitable! 

# How does it work?

1. Set up a GroupMe with a group of friends
2. Learn about investing and stocks
3. Choose stocks with the help of Onu
4. Buy a stock directly through GroupMe using Onu
5. Keep track of your portfolio through the UI

The app interacts with a CapitalOne _trust_ account that is the central place for your group investing.

# Technical Details

Our python server(Bot/Bot.py) is the main server that runs our whole bot.

#### APIs and Frameworks Used
 - [CapitalOne Nessie API](http://api.reimaginebanking.com/) for coolness and very essential stuff
 - [GroupMe](https://dev.groupme.com) API for chat
 - [API.AI](https://api.ai) for natural language processing
 - [Quandl](https://www.quandl.com/data/SF1-Core-US-Fundamentals-Data/documentation/about) for stock data
 - [Bing](https://www.bing.com) for news 
 - [Mailgun](https://www.mailgun.com) for email confirmations
 - [Flask](https://www.fullstackpython.com/flask.html) for UI
 - [Bootstrap](http://getbootstrap.com) for UI
 - [SB 2 Admin](https://github.com/kaushikraj/sb-admin-2-flask-admin) for UI
 - [ngrok](https://ngrok.com) for securing UI
 
 # How to run this bot and UI
 The keys, group id, and authentication tokens need to be filled in prior to starting  the program. These can be set up in the config.json file.
 To run the bot:
 '''
 git clone https://github.com/C1-SoftwareEngineeringSummit/team3.git
 cd Bot
 python3 bot.py
 '''
 To run the UI:
 
 
 #### Team Members: Kyle Feng, Ben Stobaugh, Kim Santiago, Kobi Felton, Glory Jain
 **Disclaimer: The creators of this app are not responsible for any financial losses/damages
incurred through the use of this app.**
