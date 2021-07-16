import tweepy, json, sqlite3, os
from web3 import Web3
from datetime import datetime
from config import CONSUMER_KEY, INFURA_URL, ETHERSCAN_TOKEN, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
from token_addresses import *
from get_data_functions import *

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
# Create API object
api = tweepy.API(auth)

print(f'Connected to Web3? {w3.isConnected()}')
print(f'Current eth blocknumber -> {w3.eth.blockNumber}')

now = datetime.now()
today9am = now.replace(hour=9, minute=0, second=0, microsecond=0)
today905am = now.replace(hour=9, minute=5, second=0, microsecond=0)
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("current date and time -> ", dt_string) 

connection = sqlite3.connect(os.path.abspath('fli.db'))
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

# class product():
    # todo create the products as a class and give the parameters as values
#   pass

def main():
  """
  main
  """
  ETHgetCurrentSupply = getCurrentSupply(ETHFLI_TOKEN_ADDRESS)
  ETHgetTotalSupply = getTotalSupply(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)
  ETHgetCurrentLeverageRatio = getCurrentLeverageRatio(ETHFLI_STRATEGY_ADAPTER_ADDRESS)
  BTCgetCurrentSupply = getCurrentSupply(BTCFLI_TOKEN_ADDRESS)
  BTCgetTotalSupply = getTotalSupply(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)
  BTCgetCurrentLeverageRatio = getCurrentLeverageRatio(BTCFLI_STRATEGY_ADAPTER_ADDRESS)
  
  
  #If time == 9am twitter post supply
  if now > today9am and now < today905am:
    print(ETH_Supply())
    print(BTC_Supply())
  
  # if supply cap is at x% then twitter post
  if round(ETHgetCurrentSupply/ETHgetTotalSupply*100) >=90:
    if now.hour % 6 == 0:
      print(ETHsupplyCapWarningThreshold())
    
  if round(BTCgetCurrentSupply/BTCgetTotalSupply*100) >=90:
    if now.hour % 6 == 0:
      print(BTCsupplyCapWarningThreshold())
  
  #pull latest max supply and compare to current max supply if not == then twitter post and update current max supply  
  cursor.execute("""
    SELECT maxSupply FROM parameters where product_id=2
  """)

  rows = cursor.fetchall()
  parameters_in_db = [row['maxSupply'] for row in rows] # list comprehension
  # print(parameters_in_db)
  if parameters_in_db[-1] != BTCgetTotalSupply:
    print(BTCmaxSupplyChange(parameters_in_db[-1],BTCgetTotalSupply))
    # cursor.execute(f"UPDATE parameters SET maxSupply = {BTCgetTotalSupply} WHERE product_id = 2")
    # connection.commit()
  
  cursor.execute("""
    SELECT maxSupply FROM parameters where product_id=1
  """)

  rows = cursor.fetchall()
  parameters_in_db = [row['maxSupply'] for row in rows] # list comprehension
  if parameters_in_db[-1] != ETHgetTotalSupply:
    print(ETHmaxSupplyChange(parameters_in_db[-1],ETHgetTotalSupply)) 
    # cursor.execute(f"UPDATE parameters SET maxSupply = {ETHgetTotalSupply} WHERE product_id = 1")
    # connection.commit()
    
  #compare current leverage ratio and if past ripcord threshold then twitter post
  if float(ETHgetCurrentLeverageRatio) > float(getIncentive(ETHFLI_STRATEGY_ADAPTER_ADDRESS)):
    print(ETHpastRipcordTolerence()) 
  
  if float(getCurrentLeverageRatio(BTCFLI_STRATEGY_ADAPTER_ADDRESS)) > float(getIncentive(BTCFLI_STRATEGY_ADAPTER_ADDRESS)):
    print(BTCpastRipcordTolerence()) 
  
  ethNAV = getNetAssetValue(getTotalComponentsRealUnitsCETHToken(ETHFLI_TOKEN_ADDRESS,cETH_ADDR),getTotalComponentsRealUnitsUSDC(ETHFLI_TOKEN_ADDRESS,UDSC_ADDR),coinGeckoPriceData(cETH_COINGECKO_ID))
  ethCoinGeckoPrice = coinGeckoPriceData(ETHFLI_COINGECKO_ID)
  ethNAVDiff = round(NAVDiff(ethNAV,ethCoinGeckoPrice),2)
  btcNAV = getNetAssetValue(getTotalComponentsRealUnitsCWBTCToken(BTCFLI_TOKEN_ADDRESS,cWBTC_ADDR),getTotalComponentsRealUnitsUSDC(BTCFLI_TOKEN_ADDRESS,UDSC_ADDR),coinGeckoPriceData(cWBTC_COINGECKO_ID))
  btcCoinGeckoPrice = coinGeckoPriceData(BTCFLI_COINGECKO_ID)
  btcNAVDiff = round(NAVDiff(btcNAV,btcCoinGeckoPrice),2)
  
  
  # print(ethNAV,ethCoinGeckoPrice)
  # print('----')
  # print(btcNAV,btcCoinGeckoPrice)
  # print(ethNAVDiff)
  
  # nav = 72
  #Tweet about net asset value disconnect
  #or (100 - (coinGeckoPriceData(ETHFLI_COINGECKO_ID) / nav) < - 2)
  # if abs((1 - (coinGeckoPriceData(ETHFLI_COINGECKO_ID) / 
  #              getNetAssetValue(getTotalComponentsRealUnitsCETHToken(ETHFLI_TOKEN_ADDRESS,cETH_ADDR),getTotalComponentsRealUnitsUSDC(ETHFLI_TOKEN_ADDRESS,UDSC_ADDR),coinGeckoPriceData(ETHFLI_COINGECKO_ID))))) > 0.02:
  #             # getNetAssetValue(getTotalComponentsRealUnitsCETHToken(ETHFLI_TOKEN_ADDRESS,cETH_ADDR),getTotalComponentsRealUnitsUSDC(ETHFLI_TOKEN_ADDRESS,UDSC_ADDR),coinGeckoPriceData(cETH_COINGECKO_ID))
  if ethNAVDiff > 2.1:
    print(ETHnetAssetValueThreshold(ethNAVDiff))
    
  if btcNAVDiff > 2.1:
    print(BTCnetAssetValueThreshold(btcNAVDiff))
  
  cursor.execute("INSERT INTO parameters (product_id, date, maxSupply, currentSupply, currentLeverageRatio) VALUES (?,?,?,?,?)",(1, dt_string,ETHgetTotalSupply,ETHgetCurrentSupply,ETHgetCurrentLeverageRatio))
  cursor.execute("INSERT INTO parameters (product_id, date, maxSupply, currentSupply, currentLeverageRatio) VALUES (?,?,?,?,?)",(2, dt_string,BTCgetTotalSupply,BTCgetCurrentSupply,BTCgetCurrentLeverageRatio))

  connection.commit()

main()

