"""
Simple UI that fetches and counts algorand addresses with a quantity of an ASA above a threshold 

When run as a script, the user will be prompted to inpur the Algorand ASA ID.  Then, it will return
some information of the asset, including the asset name. Thereafter it prompts the user to input
the balance threshold of interest.  It will fetch the results, and print the time elapsed and 
the number of addresses with an ASA balance greater than the input.

Author: Connor John Schmitz
Date:   11/20/21
"""

import json
from algosdk.v2client import indexer
from pytictoc import TicToc
import time

#Client
myindexer = indexer.IndexerClient(indexer_token="", indexer_address='https://algoexplorerapi.io/idx2/', headers={'User-Agent':'DerpaDerpBeepBoop'})
t = TicToc()

#Input Parameters
input1 = input("Input ASA ID: ")
response = myindexer.search_assets(asset_id=input1)
asset = response['assets'][0]
params = asset['params']
print("ASA Name: ", params.get('name'))
decimals = params.get('decimals')
print("ASA Decimals: "+ str(decimals))
#Indexer removes decimals, so must we.  But; ASAs may have different decimal values.  Must amend our input.
string = str(input("Input Minimum Quantity[integers only]: "))
input2 = string.ljust(decimals + len(string), '0')

#Fetch and count addresses using paginated results.
#Time the loop.
nexttoken = ""
numbal = 1
count = 0   
t.tic()

while numbal > 0:
    response = myindexer.asset_balances(asset_id=input1, min_balance=input2, next_page=nexttoken, limit=25)
    for i in response['balances']:
        count += 1
        print("Fetching addresses: ", count)
    balances = response['balances']
    numbal = len(balances)
    if numbal > 0:
        nexttoken = response.get('next-token')

#Unecessary fireworks
print("")
time.sleep(1)
print(".")
time.sleep(.15)
print("..")
time.sleep(.15)  
print("...")
time.sleep(.15)
t.toc()
time.sleep(.15)
print("...")
time.sleep(.15)
print("..")
time.sleep(.15)  
print(".")
time.sleep(.15) 
print("")
print("There are " + str(count) + " addresses with the specified parameters.")
print("")

    


