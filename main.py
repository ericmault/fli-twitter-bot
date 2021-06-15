import tweepy
import requests
import json
from web3 import Web3
from datetime import datetime
from config import CONSUMER_KEY, INFURA_URL, ETHERSCAN_TOKEN, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

ETHFLI_TOKEN_ADDRESS = "0xaa6e8127831c9de45ae56bb1b0d4d4da6e5665bd"
ETHFLI_MANAGER_ADDRESS = "0x445307De5279cD4B1BcBf38853f81b190A806075"
ETHFLI_STRATEGY_ADAPTER_ADDRESS = "0x1335D01a4B572C37f800f45D9a4b36A53a898a9b"
ETHFLI_FEE_ADAPTER_ADDRESS = "0x26F81381018543eCa9353bd081387F68fAE15CeD"
ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS = "0x0F1171C24B06ADed18d2d23178019A3B256401D3"

BTCFLI_TOKEN_ADDRESS = "0x0b498ff89709d3838a063f1dfa463091f9801c2b"
BTCFLI_MANAGER_ADDRESS = "0xC7Aede3B12daad3ffa48fc96CCB65659fF8D261a"
BTCFLI_STRATEGY_ADAPTER_ADDRESS = "0x4a99733458349505A6FCbcF6CD0a0eD18666586A"
BTCFLI_FEE_ADAPTER_ADDRESS = "0xA0D95095577ecDd23C8b4c9eD0421dAc3c1DaF87"
BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS = "0x6C8137F2F552F569CC43BC4642afbe052a12441C"


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

w3 = Web3(Web3.HTTPProvider(INFURA_URL))

print(f'Connected to Web3? {w3.isConnected()}')
print(f'Current eth blocknumber -> {w3.eth.blockNumber}')

now = datetime.now()
 
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("current date and time -> ", dt_string) 

# Create API object
api = tweepy.API(auth)



# uses etherscan API to pull total token supply
def etherscanTokenSupply():
  response = requests.get(f"https://api.etherscan.io/api?module=stats&action=tokensupply&contractaddress=0xaa6e8127831c9de45ae56bb1b0d4d4da6e5665bd&apikey={ETHERSCAN_TOKEN}")
  data3 = json.loads(response.text)
  supply = int(data3['result'])/1000000000000000000
  return(f'the current total supply for ETH2x-FLI is {supply}')

def getAbi(contractAddress):
  response = requests.get(f"https://api.etherscan.io/api?module=contract&action=getabi&address={contractAddress}&apikey={ETHERSCAN_TOKEN}")
  json_data = json.loads(response.text)
  return((json_data['result']))

def getContract(address):
  contract = w3.eth.contract(address=address, abi=getAbi(address))
  return contract

def getTotalSupply(address):
  check = w3.toChecksumAddress(address)
  contract = w3.eth.contract(address=check, abi=getAbi(address))
  execut = contract.functions.totalSupply().call()
  execut_rounded = int(execut/1000000000000000000)
#   print(f'The current total supply is {execut_rounded}')
  return(f'The current total supply is {execut_rounded}')
  
def getCurrentLeverageRatio(address):
  contract = w3.eth.contract(address=address, abi=getAbi(address))
  leverageRatio = contract.functions.getCurrentLeverageRatio().call()
  leverageRatioRounded = round(leverageRatio/1000000000000000000,2)
#   print(f'the current leverage ratio is {leverageRatioRounded}')
  return(f'{leverageRatioRounded}')

def getGetExecution(address):
  contract = w3.eth.contract(address=address, abi=getAbi(address))
  execut = contract.functions.getExecution().call()
  unutilizedLeveragePercent = int(execut[0]/1000000000000000000)
  twapMaxTradeSize = int(execut[1]/1000000000000000000)
  coolDownPeriod = int(execut[2])
  slippageAllowance = int(execut[3]/1000000000000000000)
  exchangeName = execut[4]
#   print(f'This is unutilized leverage percentage {unutilizedLeveragePercent} and this is twapmaxtradesize {twapMaxTradeSize}, and here is cooldown {coolDownPeriod}, and here is slippage tolerence {slippageAllowance} and here is exchangeName {exchangeName}')
  return(f'{execut}')
  
def getCurrentAndTotalSupply(address,address1):
  check = w3.toChecksumAddress(address)
  contract = w3.eth.contract(address=check, abi=getAbi(address))
  execut = contract.functions.totalSupply().call()
  contract2 = w3.eth.contract(address=address1, abi=getAbi(address1))
  execut = contract.functions.totalSupply().call()
  execut2 = contract2.functions.supplyCap().call()
  current_supply = int(execut/1000000000000000000)
  supply_cap = int(execut2/1000000000000000000)
#   print(f'The current supply is {current_supply} out of a max of {supply_cap}')
  return(f'{current_supply} / {supply_cap}')

# getCurrentLeverageRatio(ETHFLI_STRATEGY_ADAPTER_ADDRESS)

# getGetExecution(ETHFLI_STRATEGY_ADAPTER_ADDRESS)

# getTotalSupply(ETHFLI_TOKEN_ADDRESS)

# getCurrentAndTotalSupply(ETHFLI_TOKEN_ADDRESS,ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)


# Create a tweet
api.update_status("----- ETH2x-FLI -----\n Current Leverage Ratio -> "+ getCurrentLeverageRatio(ETHFLI_STRATEGY_ADAPTER_ADDRESS)+"\n Current Supply / Max Supply -> "+ getCurrentAndTotalSupply(ETHFLI_TOKEN_ADDRESS,ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)+ "\n ----- BTC2x-FLI -----\n Current Leverage Ratio -> "+ getCurrentLeverageRatio(BTCFLI_STRATEGY_ADAPTER_ADDRESS)+"\n Current Supply / Max Supply -> "+ getCurrentAndTotalSupply(BTCFLI_TOKEN_ADDRESS,BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)+ "\n")

