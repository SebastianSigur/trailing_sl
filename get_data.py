from lxml import html
import requests
#current_price = 0
#page = requests.get('https://finance.yahoo.com/quote/BTC-USD?p=BTC-USD&.tsrc=fin-srch')
#price = tree.xpath('//span[@data-reactid="32"]/text()')[0]

def get_data_from_website(url, xpath):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    price = tree.xpath(xpath)
    price[0] = price[0].replace(',', '')
    return price


