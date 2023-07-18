import platform

import aiohttp
import argparse
import asyncio
from datetime import date, timedelta


"""
--request [-r] default request = 1
--currency [-c] default currensy = ['EUR', 'USD']
"""

parser = argparse.ArgumentParser(description="Sorting folder")
parser.add_argument("--requests", "-r", help="Number of requests", default=1)
parser.add_argument("--currency", "-c", help="Add currency", default=None)
args = vars(parser.parse_args())
count = int(args.get("requests"))
new_currensy = args.get("currency")

URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='
list_currency = ['EUR', 'USD']


def request_limit(count):
    if count > 10:
        print("The maximum number of requests is 10!")
        quit()
    print(f'Sending {count} requests to Privatbank!')


def add_currency(list_currency, new_currensy):
    list_currency_bank = ["AUD", "AZN", "BYN", "CAD", "CHF", "CNY", "CZK", "DKK", "EUR", "GBP", "GEL", "HUF", "ILS", "JPY", "KZT", "MDL", "NOK", "PLN", "SEK", "SGD", "TMT", "TRY", "USD", "UZS", "XAU"]
    if new_currensy in list_currency_bank:
        list_currency.append(new_currensy)
        print(list_currency)
        return list_currency
    elif new_currensy == None:
        return list_currency
    print(f"Currency {new_currensy} is not in the bank's list!")
    quit()


def make_list_url(URL, count):
    list_url = list()
    current_date = date.today()
    while True:
        str_date = current_date.strftime("%d.%m.%Y")
        new_url = URL + str_date
        list_url.append(new_url)
        count -= 1
        if count == 0:
            break
        current_date -= timedelta(days=1)
    return list_url


def filter_money(list_currency, response_bank):
    list_response = list()
    for currency in list_currency:
        res = [k for k in filter(lambda el: el['currency'] == currency, response_bank['exchangeRate'])]
        one_dict = {currency: {'sale': res[0]['saleRateNB'], 'purchase': res[0]['purchaseRateNB']}}
        list_response.append(one_dict)
    dict_response = {response_bank['date'] : list_response}
    return dict_response
    

async def request_privat(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                response_bank = await response.json()
                result = filter_money(list_currency, response_bank)
                return result
            else:
                print("No data available for the selected date")
    except aiohttp.ClientConnectorError as err:
        print(f'Connection error: {url}', str(err))


async def main():
    async with aiohttp.ClientSession() as session:
        list_request = list()
        list_url_for_request = make_list_url(URL, count)
        for url in list_url_for_request:
            list_request.append(request_privat(session, url))
        response_session = await asyncio.gather(*list_request)
        print(response_session)
                    

if __name__ == "__main__":
    request_limit(count)
    list_currency = add_currency(list_currency, new_currensy)
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
