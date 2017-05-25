import locale
import quandl

locale.setlocale(locale.LC_ALL, ('en_US', 'UTF-8'))

# Returns price info in a pandas DataFrame
def get_stock_info(ticker):
    return quandl.get('WIKI/' + ticker.upper()).tail(1)

# Returns end-of-day stock price from the previous day
def get_stock_price(ticker):
    return get_stock_info(ticker)['Close'].tolist()[0]

# Returns stock price in a user-friendly way
# https://stackoverflow.com/questions/320929/currency-formatting-in-python
def get_stock_price_friendly(ticker):
    ticker = ticker.upper()
    try:
        price = get_stock_price(ticker)
        price_pretty = locale.currency(price)
        return "Yesterday's end-of-day price for %s is %s." % (ticker, price_pretty)
    except quandl.errors.quandl_error.NotFoundError:
        return "Sorry, %s is not a valid ticker symbol name." % ticker

# debug
print get_stock_price_friendly('AAPL')
print get_stock_price_friendly('QWERTY')
