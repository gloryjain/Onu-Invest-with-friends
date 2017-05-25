#!/usr/bin/python
import sys

def getUrl(ticker):
	ticker = ticker.strip().upper()
	url = "https://finance.yahoo.com/quote/" + ticker + "/?p=" + ticker
	return url;

def getUserInput():
	ticker = raw_input("Enter the ticker:")
	print(getUrl(ticker))


getUserInput()