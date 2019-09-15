import math
from random import random

STEAM_FEE = 0.05
CSGO_FEE = 0.10


def getPayoutFromPrice(price):
    return round(price - getTotalFeeFromPrice(price), 2)


def getPriceFromPayout(payout):
    return round(payout + getTotalFeeFromPayout(payout), 2)


def getTotalFeeFromPrice(price):
    for i in reversed(range(0, int(price * 100), 1)):
        current_payout = i/100
        if round(getTotalFeeFromPayout(current_payout) + current_payout, 2) == round(price, 2):
            return round(getTotalFeeFromPayout(current_payout), 2)
    return 0.0



def getTotalFeeFromPayout(payout):
    steam_transaction_fee = math.floor((payout * STEAM_FEE) * 100) / 100
    csgo_transaction_fee = math.floor((payout * CSGO_FEE) * 100) / 100
    if steam_transaction_fee == 0: steam_transaction_fee = 0.01
    if csgo_transaction_fee == 0: csgo_transaction_fee = 0.01
    return steam_transaction_fee + csgo_transaction_fee




def test():
    """
    This function shows test values for the provided functions to compare with the steam market
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
