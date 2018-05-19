import json
import requests as r


class CoinMarketCapApiHelper:

    def __init__(self, base_url):
        self.baseUrl = base_url

    def get_base_url(self):
        return self.baseUrl

    def get_listings(self):
        response = r.get(self.get_base_url() + 'listings/')
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return False

    def get_currency_ticker(self, id):
        response = r.get(self.get_base_url() + 'ticker/' + id + '/')
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return False


base_url = 'https://api.coinmarketcap.com/v2/'
client = CoinMarketCapApiHelper(base_url)
parsed_response = client.get_listings()
data = parsed_response['data']

currency_dictionary = {}

for datum in data:
    if "symbol" in datum and "id" in datum and "symbol" not in currency_dictionary:
        symbol = datum["symbol"]
        currency_dictionary[symbol] = datum["id"]
    else:
        continue

# get a real currency token
invalid_input = True

while invalid_input:
    token = input("Enter a currency symbol to view: \n")
    parsed_response = client.get_currency_ticker(str(currency_dictionary[token]))
    if parsed_response is not False:
        invalid_input = False
        data = parsed_response['data']
        print(data)
    else:
        print('Invalid token')






