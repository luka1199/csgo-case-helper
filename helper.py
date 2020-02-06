import utils
import requests
from math import ceil
from case import Case
import json
import sys
import time

class Helper:
    def __init__(self):
        pass

    def getCases(self):
        """Returns all CS:GO cases listed on the steam market.
        
        Returns:
            list -- A list of all cases currently listed on the steam market.
        """
        cases = []
        res = requests.get(
            "https://steamcommunity.com/market/search/render/?query=container+case&sort_column=default&sort_dir=desc&appid=730&norender=1&count=100")
        results = json.loads(res.text)
        if results["success"] == "false":
            raise Exception("Something went wrong")
        for case in results["results"]:
            cases.append(Case(case["name"], case["sell_listings"], case["sell_price"]/100))
        return cases
    
    def getItemPrice(self, name):
        """Returns the steam market price of the given item.

        Returns:
            float -- The price of the item.
        """
        res = requests.get(
            "https://steamcommunity.com/market/search/render/?query={}&sort_column=default&appid=730&norender=1&count=100".format(
                name
            ))
        results = json.loads(res.text)

        if results["success"] == "false":
            raise Exception("Something went wrong")
        price = 0
        if len(results["results"]) > 0:
            price = results["results"][0]["sell_price"]/100
        return price


    def getInventory(self, steamid):
        """Returns inventory of the user with the given steamid.
        
        Arguments:
            steamid {string} -- The Steam ID of the user you want to get the Inventory from.
        
        Returns:
            list -- A list of tuples containing item name and amount.
        """
        data = requests.get(
            "https://steamcommunity.com/id/{}/inventory/json/730/2?l=english&count=5000".format(steamid))
        json_data = json.loads(data.text)
        try:
            descriptions = json_data["rgDescriptions"]
        except:
            return None
        inventory = {}
        for item in descriptions:
            inventory[descriptions[item]["market_name"]] = self.getItemAmount(descriptions[item]["classid"], json_data)
        return inventory


    def getItemAmount(self, classid, json_data):
        """Returns the amount of items with the given class ID in the inventory.
        
        Arguments:
            classid {string} -- The class ID of the item you want to get the amount of.
            json_data {dict} -- The json data from the steam inventory endpoint.
        
        Returns:
            int -- The amount of items with given the class ID in the inventory.
        """
        inventory = json_data["rgInventory"]
        count = 0
        for item in inventory:
            if inventory[item]["classid"] == classid:
                count += 1
        return count

    def printInventory(self, steamid):
        """Prints out the inventory of the user with the given steamid.
        
        Arguments:
            steamid {string} -- The Steam ID of the user you want to print out the Inventory from.
        """
        inventory = self.getInventory(steamid)
        if inventory is None:
            print("Error: Can't get inventory of {}.".format(steamid))
        else:
            print("\n" + "-" * 50)
            print("CS:GO Inventory of {}: \n".format(steamid))
            for name, amount in inventory.items():
                print("  ", name, " ({}) -> {}$".format(amount, self.getItemPrice(name)*amount), sep="")
                # 69 requests per minute allowed
                # time.sleep(1)
            print("-" * 50, "\n", sep="")


    def getBestInvestments(self, count=5):
        """Returns the best CS:GO cases to currently invest in.

        The function considers the price and the listed amount of all cases listed on the steam market.
        
        Keyword Arguments:
            count {int} -- The amount of best cases you want to get returned. (default: {5})
        
        Returns:
            list -- A list containing cases.
        """
        cases = self.getCases()

        # Sort by amount on market (ASC)
        cases.sort(key=lambda x: x.get_amount())
        cases.sort(key=lambda x: x.get_price())
        return cases[0:min(len(cases) - 1, count)]


    def printBestInvestments(self, count=5):
        """Prints out the best CS:GO cases to currently invest in.
        
        Keyword Arguments:
            count {int} -- The amount of best cases you want to print out. (default: {5})
        """
        print("\n" + "-" * 50)
        print("Best case investments: \n")
        for i, case in enumerate(self.getBestInvestments(count)):
            print("{}. {}".format(i + 1, case))
        print("-" * 50, "\n", sep="")


if __name__ == "__main__":
    helper = Helper()
    
    if len(sys.argv) == 1:
        helper.printBestInvestments(count=10)
        # print(helper.getItemPrice("P250 | Boreal Forest (Field-Tested)"))

    if len(sys.argv) == 2:
        if sys.argv[1] == "help":
            print("Usage: python helper.py [<steamid> or help]")
            sys.exit()
        else:
            helper.printInventory(sys.argv[1])

