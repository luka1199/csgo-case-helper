import utils
import requests
from math import ceil
from case import Case
import json

STEAMID = "luka111599"


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


def getInventory(steamid):
    data = requests.get(
        "https://steamcommunity.com/id/{}/inventory/json/730/2?l=english&count=5000".format(steamid))
    json_data = json.loads(data.text)
    try:
        descriptions = json_data["rgDescriptions"]
    except:
        return None
    inventory = {}
    for item in descriptions:
        inventory[descriptions[item]["name"]] = getItemAmount(descriptions[item]["classid"], json_data)
    return inventory


def getItemAmount(classid, json_data):
    inventory = json_data["rgInventory"]
    count = 0
    for item in inventory:
        if inventory[item]["classid"] == classid:
            count += 1
    return count


def printInventory(steamid):
    inventory = getInventory(steamid)
    if inventory is None:
        print("Error: Can't get inventory of {}.".format(steamid))
    else:
        print("\n" + "-" * 50)
        print("CS:GO Inventory of {}: \n".format(steamid))
        for name, amount in inventory.items():
            print("  ", name, " ({})".format(amount), sep="")
        print("-" * 50, "\n", sep="")


def getBestInvestments(cases, count=5):    
    # Sort by amount on market (ASC)
    cases.sort(key=lambda x: x.get_amount())
    cases.sort(key=lambda x: x.get_price())
    return cases[0:count]


def printBestInvestments(cases, count=5): 
    print("\n" + "-" * 50)
    print("Best case investments: \n")
    for i, case in enumerate(getBestInvestments(cases, count)):
        print("{}. {}".format(i + 1, case))
    print("-" * 50, "\n", sep="")


if __name__ == "__main__":
    cases = getCases()
    printBestInvestments(cases, 10)
    printInventory(STEAMID)
