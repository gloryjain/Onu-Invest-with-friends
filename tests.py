from Tools.pgYahoo import getUrl, getUserInput
from Tools.stock_price import get_stock_info, get_stock_price, get_stock_price_friendly

#Test Yahoo Finance Link function
url = 'Correct Url' + getUrl('AAPL')
print(url)
url = 'Should be an error message:' + getUrl('IPSEMDOLSET')
print(url)

#Test Stock Price functions
price = get_stock_info('AAPL')
print("The price of Apple:")
print(price)

price = + get_stock_price('AAPL')
print('The price of Apple')
print(price)

price =  get_stock_price_friendly('AAPL')
print(price)
