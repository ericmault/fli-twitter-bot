import requests
import json
from web3 import Web3
from datetime import datetime
from config import INFURA_URL, ETHERSCAN_TOKEN
from token_addresses import *


w3 = Web3(Web3.HTTPProvider(INFURA_URL))

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

def getCurrentSupply(address):
  check = w3.toChecksumAddress(address)
  contract = w3.eth.contract(address=check, abi=getAbi(address))
  execut = contract.functions.totalSupply().call()
  current_supply = int(execut/1000000000000000000)
#   print(f'The current supply is {current_supply} out of a max of {supply_cap}')
  return(current_supply)

def getTotalSupply(address):
  check = w3.toChecksumAddress(address)
  contract2 = w3.eth.contract(address=address, abi=getAbi(address))
  execut2 = contract2.functions.supplyCap().call()
  supply_cap = int(execut2/1000000000000000000)
#   print(f'The current supply is {current_supply} out of a max of {supply_cap}')
  return(supply_cap)

def ETH_Supply():
  return("----- ETH2x-FLI -----\nCurrent Supply / Max Supply -> "+ getCurrentAndTotalSupply(ETHFLI_TOKEN_ADDRESS,ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)+ "\nCurrently at ~" +str(round((getCurrentSupply(ETHFLI_TOKEN_ADDRESS)/getTotalSupply(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)*100)))+"% of max supply\nLearn more about the supply cap and why it is important here: https://docs.indexcoop.com/community/governance/fli-strategy-parameter-updates")

def BTC_Supply():
  return("----- BTC2x-FLI -----\nCurrent Supply / Max Supply -> "+ getCurrentAndTotalSupply(BTCFLI_TOKEN_ADDRESS,BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)+ "\nCurrently at ~" +str(round((getCurrentSupply(BTCFLI_TOKEN_ADDRESS)/getTotalSupply(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)*100)))+"% of max supply\nLearn more about the supply cap and why it is important here: https://docs.indexcoop.com/community/governance/fli-strategy-parameter-updates")

def maxSupplyChange():
  
  #The max supply cap for <TOKEN>2x-FLI has been changed to ###### from #######

  #Learn more about the supply cap and why it is important here: https://docs.indexcoop.com/community/governance/fli-strategy-parameter-updates
  pass

def pastRipcordTolerence():
  pass
#<TOKEN>2x-FLI has fallen outside of its leverage tolerance, anyone can rebalance immediately for reward! 

#See docs here: https://docs.indexcoop.com/resources-beta/technical-overview/fli-technical-documentation/fli-keeper-bot-integration

def supplyCapWarningThreshold():
  pass

#CAUTION! <TOKEN>2x-FLI is at ##% of it’s supply cap. When Supply cap is reached there can be a disconnect from net asset value and traded value. 

#Read more here: https://medium.com/indexcoop/understanding-the-eth2x-fli-premium-4ac8c5f6faa1

def netAssetValueThreshold():
  #ATTENTION! There is currently a ##.#% premium on <TOKEN>2x-FLI compared to it’s net asset value. 
  pass
  #Read more here: https://medium.com/indexcoop/understanding-the-eth2x-fli-premium-4ac8c5f6faa1
