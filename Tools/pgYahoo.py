#!/usr/bin/python
import sys

def getUrl(ticker):
	if type(ticker) == str and len(ticker) <= 5:
		ticker = ticker.strip().upper()
		url = "https://finance.yahoo.com/quote/" + ticker + "/?p=" + ticker
		return url
	else:
		return 'Please enter a properly formatted ticker'


def getUserInput():
	ticker = raw_input("Enter the ticker:")
	print(getUrl(ticker))


#getUserInput()
