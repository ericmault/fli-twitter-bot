import tweepy
import requests
import json
import sqlite3
from web3 import Web3
from datetime import datetime
from config import CONSUMER_KEY, INFURA_URL, ETHERSCAN_TOKEN, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
from token_addresses import *
from get_data_functions import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

print(f'Connected to Web3? {w3.isConnected()}')
print(f'Current eth blocknumber -> {w3.eth.blockNumber}')

now = datetime.now()

dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("current date and time -> ", dt_string) 

# Create API object
api = tweepy.API(auth)

# getCurrentLeverageRatio(ETHFLI_STRATEGY_ADAPTER_ADDRESS)

# getGetExecution(ETHFLI_STRATEGY_ADAPTER_ADDRESS)

# getTotalSupply(ETHFLI_TOKEN_ADDRESS)

# getCurrentAndTotalSupply(ETHFLI_TOKEN_ADDRESS,ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)


def do_stuff():
  #api.update_status("----- ETH2x-FLI -----\n Current Leverage Ratio -> "+ getCurrentLeverageRatio(ETHFLI_STRATEGY_ADAPTER_ADDRESS)+"\n Current Supply / Max Supply -> "+ getCurrentAndTotalSupply(ETHFLI_TOKEN_ADDRESS,ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)+ "\n ----- BTC2x-FLI -----\n Current Leverage Ratio -> "+ getCurrentLeverageRatio(BTCFLI_STRATEGY_ADAPTER_ADDRESS)+"\n Current Supply / Max Supply -> "+ getCurrentAndTotalSupply(BTCFLI_TOKEN_ADDRESS,BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)+ "\n")
# Create a tweet
  # api.update_status(ETH_Supply())
  print(ETH_Supply())
  print(BTC_Supply())
  #print(str(round(getCurrentSupply(ETHFLI_TOKEN_ADDRESS)/getTotalSupply(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)*100)))
  print("done")


# class product():
#   pass

def main():
  #If time == 9am twitter post supply
  
  # if supply cap is at x% then twitter post
  
  #pull latest max supply and compare to current max supply if not == then twitter post and update current max supply
  
  #compare current leverage ratio and if past ripcord threshold then twitter post
  
  #Tweet about net asset value disconnect
  
  
do_stuff()
# ----- <TOKEN>2x-FLI -----
# Current Supply / Max Supply -> ###### / ######
# Currently at ##% of max supply
