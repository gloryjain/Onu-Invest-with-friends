import locale
from datetime import *
import quandl
import matplotlib.pyplot as plt
import pandas as pd
from IPython import embed
locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8')) # Set locale to en_US
quandl.ApiConfig.api_key = "V5uEXA4L1zfc9Q6Dp9Lz" # Set API key

def get_stock_info(ticker, dataset, suffix, start_date='', end_date='', returns=''):
    #embed()
    try:
        demo = quandl.get(dataset + '/' + ticker.upper() + suffix, start_date=start_date, end_date=end_date, returns=returns)
    except quandl.errors.quandl_error.ForbiddenError or quandl.errors.quandl_error.NotFoundError:
        demo = None
    return demo

# Get Earnings
tickers = []
earnings = []

for line in open('NASDAQ.txt'):
    ticker = line[0:3]
    print(ticker)
    ticker = ticker.rstrip(' ')
    tickers.append(ticker)
    data = get_stock_info(ticker, dataset='SF1', suffix='_EPS_MRQ')
    if data is not None:
        datum = data['Value'].iloc[-1]
        earnings.append(datum)
