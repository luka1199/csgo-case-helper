import math
from random import random

STEAM_FEE = 0.05
CSGO_FEE = 0.10


def getPayoutFromPrice(price):
    """Returns the payout you get on the steam market for selling an item for
    the given price.
    
    Arguments:
        price {float} -- The price the buyer pays to buy your item.
    
    Returns:
        float -- The payout you get for selling an item for the given price.
    """
    return round(price - getTotalFeeFromPrice(price), 2)


def getPriceFromPayout(payout):
    """Returns the price you have to list an item for on the steam market to
    get the given payout.
    
    Arguments:
        payout {float} -- The payout you want to get.
    
    Returns:
        float -- The price you have to list an item for on the steam market to
            get the given payout.
    """
    return round(payout + getTotalFeeFromPayout(payout), 2)


def getTotalFeeFromPrice(price):
    """Returns the fee you have to pay if you sell an item on the steam market for
    given price.
    
    Arguments:
        price {float} -- The price the buyer pays to buy your item.
    
    Returns:
        float -- The fee you have to pay for selling an item on the steam market for
            the given price.
    """
    for i in reversed(range(0, int(price * 100), 1)):
        current_payout = i/100
        if round(getTotalFeeFromPayout(current_payout) + current_payout, 2) == round(price, 2):
            return round(getTotalFeeFromPayout(current_payout), 2)
    return 0.0


def getTotalFeeFromPayout(payout):
    """Returns the fee you have to pay if you sell an item on the steam market for
    given payout.
    
    Arguments:
        payout {float} -- The payout you get for selling an item.
    
    Returns:
        float -- The fee you have to pay for selling an item on the steam market for
            the given payout.
    """
    steam_transaction_fee = math.floor((payout * STEAM_FEE) * 100) / 100
    csgo_transaction_fee = math.floor((payout * CSGO_FEE) * 100) / 100
    if steam_transaction_fee == 0:
        steam_transaction_fee = 0.01
    if csgo_transaction_fee == 0:
        csgo_transaction_fee = 0.01
    return steam_transaction_fee + csgo_transaction_fee


def getProfit(buyPrice, units, sellPrice):
    """Returns the profit for selling a given amount of units.
    
    Arguments:
        buyPrice {flaot} -- The price you payed per item.
        units {int} -- The amount of items you are selling.
        sellPrice {float} -- The price the buyer pays for your items.
    
    Returns:
        float -- The profit.
    """
    investment = buyPrice * units
    profit = units * getPayoutFromPrice(sellPrice) - investment
    return round(profit, 2)


def test():
    """
    Shows test values for the provided functions to compare with the steam market.
    """
    print("\nTesting Payout --> Price")
    for i in range(10):
        payout = round(random() * 500, 2)
        print("Payout:", payout, "--> Price:", getPriceFromPayout(payout))

    print("\nTesting Price --> Payout")
    for i in range(10):
        price = round(random() * 500, 2)
        print("Price:", price, "--> Payout:", getPayoutFromPrice(price))

    print("Payout:", "0.01", "--> Price:", getPriceFromPayout(0.01))
    print("Price:", "0.03", "--> Payout:", getPayoutFromPrice(0.03))


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    xvals = []
    yvals = []
    for i in range(0, 40):
        price = i / 10
        xvals.append(price)
        yvals.append(getProfit(0.03, 836, price))

    plt.plot(xvals, yvals)
    plt.xlabel('Sell price')
    plt.ylabel('Profit')
    plt.show()
