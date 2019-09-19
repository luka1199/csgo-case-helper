import utils
import requests
from math import ceil
from case import Case
import json


def getCases():
    cases = []
    res = requests.get(
        'https://steamcommunity.com/market/search/render/?query=container+case&sort_column=default&sort_dir=desc&appid=730&norender=1&count=100')
    results = json.loads(res.text)
    if results["success"] == "false":
        raise Exception("Something went wrong")
    for case in results["results"]:

        cases.append(Case(case["name"], case["sell_listings"], case["sell_price"]/100))
    return cases


def getInvestmentIndex(case):
    return 1


def getBestInvestments(cases, count=5):    
    # Sort by amount on market (ASC)
    cases.sort(key=lambda x: x.get_amount())
    cases.sort(key=lambda x: x.get_price())
    return cases[0:count]


def getBestInvestmentIndex(cases, count=5):
    cases.sort(key=lambda x: getInvestmentIndex(x))
    return cases[0:count]


def printBestInvestments(cases, count=5): 
    print("\n" + "-" * 50)
    print("Best case investments: \n")
    for i, case in enumerate(getBestInvestments(cases, count)):
        print("{}. {}".format(i + 1, case))
    print("-" * 50, "\n", sep="")


def printBestInvestmentIndex(cases, count=5): 
    print("\n" + "-" * 50)
    print("Best case investments: \n")
    for i, case in enumerate(getBestInvestmentIndex(cases, count)):
        print("{}. {}".format(i + 1, case))
    print("-" * 50, "\n", sep="")


if __name__ == "__main__":
    cases = getCases()
    printBestInvestments(cases, 10)
    printBestInvestmentIndex(cases, 10)
