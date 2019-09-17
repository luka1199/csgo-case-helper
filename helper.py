import utils
import requests
from bs4 import BeautifulSoup
from math import ceil
from selenium import webdriver



def getCases():
    page = requests.get(
        'https://steamcommunity.com/market/search?appid=730&q=container+case')

    soup = BeautifulSoup(page.text, 'html.parser')
    total_amount = int(
        soup.find("span", attrs={'id': 'searchResults_total'}).text)

    cases = []
    cases_html = []

    for i in range(ceil(total_amount / 10)):
        browser = webdriver.PhantomJS()
        browser.get(
            'https://steamcommunity.com/market/search?appid=730&q=container+case#p{}_quantity_asc'.format(i+1))
        page = browser.page_source
        browser.close()

        soup = BeautifulSoup(page, 'html.parser')
        cases_html = soup.findAll("div", attrs={'class': 'market_listing_row market_recent_listing_row market_listing_searchresult'})
    
        for case_html in cases_html:
            soup = case_html
            case = Case(soup.find("span", attrs={'class': 'market_listing_item_name'}).text,
                        int(soup.find("span", attrs={
                            "class": "market_listing_num_listings_qty"}).text.replace(",", "")),
                        float(soup.findAll("span", attrs={"class": "normal_price"})[1].text.replace(" ", "").replace("$", "").replace("USD", "").replace(",", ".")))
            cases.append(case)
    return cases


def getBestInvestments(cases, count=5):
    result = []
    
    # Sort by amount on market (ASC)
    cases.sort(key=lambda x: x.amount)
    for case in cases:
        if case.price == 0.03:
            result.append(case)
        if len(result) == count:
            break
    for case in cases:
        if case.price == 0.04:
            result.append(case)
        if len(result) == count:
            break
    return result


def printBestInvestments(cases, count=5):
    for i, case in enumerate(getBestInvestments(cases, count)):
        print("{}. {}".format(i + 1, case))


class Case:
    def __init__(self, name, amount, price):
        self.name = name
        self.amount = amount
        self.price = price

    def __repr__(self):
        return "Case(Name: {}, Amount: {}, Price: {})".format(self.name, self.amount, self.price)

    def __str__(self):
        return "{} (Amount: {}): {}$".format(self.name, self.amount, self.price)


if __name__ == "__main__":
    cases = getCases()
    
