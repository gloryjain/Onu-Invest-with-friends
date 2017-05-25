#Function to withraw money from the individual's bank
#and then deposit in the central Onu Bank
#will then subtract from the Onu bank
#Also keeps track how much 

import requests
import json
import random

moneyToWithdraw = 0

glory = 592713b4ceb8abe24250de24
kobi = 592713c2ceb8abe24250de28
ben = 592713bfceb8abe24250de27
kyle = 592713bcceb8abe24250de26 
kim = 592713baceb8abe24250de25

group = {"glory":glory,"kobi":kobi,"ben":ben, "kyle":kyle, "kim":kim}

def changeMoney(money):
	moneyToWithdraw = money

def withdrawIndiv(customerID):
	for key, value in group.iterItems():
		print(key, value)


def depositOnu(total):