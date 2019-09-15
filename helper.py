import utils
import requests
from bs4 import BeautifulSoup
from math import ceil



def getCases():
    page = requests.get(
        'https://steamcommunity.com/market/search?appid=730&q=container+case')

    soup = BeautifulSoup(page.text, 'html.parser')
    total_amount = int(soup.find("span", attrs={'id': 'searchResults_total'}).text)
    
    print("total:", total_amount)

    cases = []

    for i in range(ceil(total_amount / 10)):
        page = i + 1

        page = requests.get(
            'https://steamcommunity.com/market/search?appid=730&q=container+case#p{}_quantity_asc'.format(page))

        soup = BeautifulSoup(page.text, 'html.parser')
        cases.extend([i.text for i in soup.findAll("span", attrs={'class': 'market_listing_item_name'})])

    print(cases)
    print(len(cases))

class Case:
    def __init__(self):
        self.name = ""
        self.amount = 0
        self.price = 0.0

if __name__ == "__main__":
    getCases()
