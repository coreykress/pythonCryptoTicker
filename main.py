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
        response = r.get(self.get_base_url() + 'ticker/' + id)
        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            return False


base_url = 'https://api.coinmarketcap.com/v2/'
client = CoinMarketCapApiHelper(base_url)

# set up dict of crypto tokens and ids
parsed_response = client.get_listings()
data = parsed_response['data']

currency_dictionary = {}

for datum in data:
    if "symbol" in datum and "id" in datum and "symbol" not in currency_dictionary:
        symbol = datum["symbol"]
        currency_dictionary[symbol] = datum["id"]
    else:
        continue

run_program = True

while run_program:
    # get a real currency token
    invalid_input = True
    crypto_token = ''

    while invalid_input:
        token = input("Enter a crypto symbol to view: \n")
        if token in currency_dictionary:
            invalid_input = False
            crypto_token = token
        else:
            print('Invalid token')

    # select a currency
    invalid_input = True

    while invalid_input:
        currency_token = input("Enter a currency to convert to (just hit enter for USD): \n")
        if len(currency_token) == 0:
            currency_token = 'USD'

        parsed_response = client.get_currency_ticker(str(currency_dictionary[crypto_token]) + '/?convert=' + currency_token)

        if not parsed_response:
            print('ERROR')
            continue
        else:
            invalid_input = False
            data = parsed_response["data"]
            # different print strategy
            print(json.dumps(data, indent=4))

    continue_program_input = input("Look up another crypto? (y/N)")

    if continue_program_input.lower() == 'n':
        print("goodbye")
        run_program = False
