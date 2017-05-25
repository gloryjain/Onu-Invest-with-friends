import locale
from datetime import *
import quandl
import matplotlib.pyplot as plt

locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8')) # Set locale to en_US
quandl.ApiConfig.api_key = "V5uEXA4L1zfc9Q6Dp9Lz" # Set API key

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
    print data
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

# debug
print get_stock_price_friendly('AAPL')
print get_stock_price_friendly('GOOG')
print get_stock_price_friendly('FB')
print get_stock_price_friendly('COF')
print get_stock_price_friendly('QWERTY')
# plot_stock_earnings('AAPL')
