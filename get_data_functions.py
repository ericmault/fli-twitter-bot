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


# struct ExecutionSettings { 
#     uint256 unutilizedLeveragePercentage;            // Percent of max borrow left unutilized in precise units (1% = 10e16)
#     uint256 twapMaxTradeSize;                        // Max trade size in collateral base units
#     uint256 twapCooldownPeriod;                      // Cooldown period required since last trade timestamp in seconds
#     uint256 slippageTolerance;                       // % in precise units to price min token receive amount from trade quantities
#     string exchangeName;                             // Name of exchange that is being used for leverage
#     bytes leverExchangeData;                         // Arbitrary exchange data passed into rebalance function for levering up
#     bytes deleverExchangeData;                       // Arbitrary exchange data passed into rebalance function for delevering
# }


def getExecution(address):
  contract = w3.eth.contract(address=address, abi=getAbi(address))
  execut = contract.functions.getExecution().call()
  unutilizedLeveragePercent = int(execut[0]/1000000000000000000)
  twapMaxTradeSize = int(execut[1]/1000000000000000000)
  coolDownPeriod = int(execut[2])
  slippageAllowance = int(execut[3]/1000000000000000000)
  exchangeName = execut[4]
#   print(f'This is unutilized leverage percentage {unutilizedLeveragePercent} and this is twapmaxtradesize {twapMaxTradeSize}, and here is cooldown {coolDownPeriod}, and here is slippage tolerence {slippageAllowance} and here is exchangeName {exchangeName}')
  return(f'This is unutilized leverage percentage {unutilizedLeveragePercent} and this is twapmaxtradesize {twapMaxTradeSize}, and here is cooldown {coolDownPeriod}, and here is slippage tolerence {slippageAllowance} and here is exchangeName {exchangeName}')

# struct IncentiveSettings {
#     uint256 etherReward;                             // ETH reward for incentivized rebalances
#     uint256 incentivizedLeverageRatio;               // Leverage ratio for incentivized rebalances
#     uint256 incentivizedSlippageTolerance;           // Slippage tolerance percentage for incentivized rebalances
#     uint256 incentivizedTwapCooldownPeriod;          // TWAP cooldown in seconds for incentivized rebalances
#     uint256 incentivizedTwapMaxTradeSize;            // Max trade size for incentivized rebalances in collateral base units
# }


def getIncentive(address):
    #currently just returning the incentivizedLeverageRatio
    #
  contract = w3.eth.contract(address=address, abi=getAbi(address))
  execut = contract.functions.getIncentive().call()
  etherReward = float(execut[0]*1e-18)
  incentivizedLeverageRatio = float(execut[1]*1e-18)
  incentivizedSlippageTolerance = float(execut[2]*1e-18)
  incentivizedTwapCooldownPeriod = float(execut[3]*1e-18)
  # incentivizedTwapMaxTradeSize = float(execut[4]*1e-18)
  #return(f'either reward {etherReward},{incentivizedLeverageRatio},{incentivizedSlippageTolerance},{incentivizedTwapMaxTradeSize}')
  return(incentivizedLeverageRatio)
  
  
#   struct MethodologySettings { 
#     uint256 targetLeverageRatio;                     // Long term target ratio in precise units (10e18)
#     uint256 minLeverageRatio;                        // In precise units (10e18). If current leverage is below, rebalance target is this ratio
#     uint256 maxLeverageRatio;                        // In precise units (10e18). If current leverage is above, rebalance target is this ratio
#     uint256 recenteringSpeed;                        // % at which to rebalance back to target leverage in precise units (10e18)
#     uint256 rebalanceInterval;                       // Period of time required since last rebalance timestamp in seconds
# }

def getMethodology(address):
  contract = w3.eth.contract(address=address, abi=getAbi(address))
  execut = contract.functions.getMethodology().call()
  #targetLeverageRatio = int(execut[0]/1000000000000000000)
  targetLeverageRatio = float(execut[0]*1e-18)
  minLeverageRatio = round(float(execut[1]*1e-18),2)
  #'{0:.3g}'.format(num)
  maxLeverageRatio = round(float(execut[2]*1e-18),2)
  recenteringSpeed = round(float(execut[3]*1e-18),2)
  rebalanceInterval = execut[4]/60
  return(f' targetleverage -> {targetLeverageRatio} minLevRatio -> {minLeverageRatio}, maxLevRatio -> {maxLeverageRatio}, recentingspeed -> {recenteringSpeed} rebalance interbal -> {rebalanceInterval}')
    
def getCurrentAndTotalSupply(address,address1):
  check = w3.toChecksumAddress(address)
  contract = w3.eth.contract(address=check, abi=getAbi(address))
  execut = contract.functions.totalSupply().call()
  contract2 = w3.eth.contract(address=address1, abi=getAbi(address1))
  execut = contract.functions.totalSupply().call()
  execut2 = contract2.functions.supplyCap().call()
  current_supply = format(int(execut/1000000000000000000),',d')
  supply_cap = format(int(execut2/1000000000000000000),',d')
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


# uses coingecko API for prices
def coinGeckoPriceData(token_id):
  response = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids={token_id}&vs_currencies=usd")
  data3 = json.loads(response.text)
  #print("$"+str(data3[f'{token_id}']['usd']))
#   print(data3[f'{token_id}']['usd'])
  return((data3[f'{token_id}']['usd']))

def getTotalComponentsRealUnitsUSDC(fli_address,underlying_address):
    check = w3.toChecksumAddress(fli_address)
    contract2 = w3.eth.contract(address=fli_address, abi=getAbi(fli_address))
    execut2 = contract2.functions.getTotalComponentRealUnits(underlying_address).call()
    components = float(execut2*1e-6)
    return(components)

def getTotalComponentsRealUnitsCWBTCToken(fli_address,underlying_address):
    check = w3.toChecksumAddress(fli_address)
    contract2 = w3.eth.contract(address=fli_address, abi=getAbi(fli_address))
    execut2 = contract2.functions.getTotalComponentRealUnits(underlying_address).call()
    components = float(execut2*1e-8)
    return(components)

def getTotalComponentsRealUnitsCETHToken(fli_address,underlying_address):
    check = w3.toChecksumAddress(fli_address)
    contract2 = w3.eth.contract(address=fli_address, abi=getAbi(fli_address))
    execut2 = contract2.functions.getTotalComponentRealUnits(underlying_address).call()
    components = float(execut2*1e-8)
    return(components)

def getNetAssetValue(wrappedPosition, stableCoinPosition,price):
    """
    use stuff here
    """
    # print(f"wrappedpost {wrappedPosition}, stable pos {stableCoinPosition}, price {price}")
    nav = wrappedPosition * price + stableCoinPosition
    # print("nav below")
    # print(nav)
    return(nav)

def NAVDiff(nav,price):
    """
    www.calculatorsoup.com/calculators/algebra/percent-difference-calculator.php
    """
    return((abs(nav-price)/(abs((nav+price)/2))*100))


# print(coinGeckoPriceData(cETH_COINGECKO_ID))
# print(getTotalComponentsRealUnitsUSDC(ETHFLI_TOKEN_ADDRESS,UDSC_ADDR))
# print(getTotalComponentsRealUnitsCETHToken(ETHFLI_TOKEN_ADDRESS,cETH_ADDR))
# print(getNetAssetValue(getTotalComponentsRealUnitsCETHToken(ETHFLI_TOKEN_ADDRESS,cETH_ADDR),getTotalComponentsRealUnitsUSDC(ETHFLI_TOKEN_ADDRESS,UDSC_ADDR),coinGeckoPriceData(cETH_COINGECKO_ID)))
# print(coinGeckoPriceData(ETHFLI_COINGECKO_ID))

# navTest = getNetAssetValue(getTotalComponentsRealUnitsCETHToken(ETHFLI_TOKEN_ADDRESS,cETH_ADDR),getTotalComponentsRealUnitsUSDC(ETHFLI_TOKEN_ADDRESS,UDSC_ADDR),coinGeckoPriceData(cETH_COINGECKO_ID))
# priceTest = coinGeckoPriceData(ETHFLI_COINGECKO_ID)

# print((navTest))
# print((priceTest))
# print(abs(navTest-priceTest)/(abs((navTest+priceTest)/2))*100)
# print('------')

# print(coinGeckoPriceData(cWBTC_COINGECKO_ID))
# print(getTotalComponentsRealUnitsUSDC(BTCFLI_TOKEN_ADDRESS,UDSC_ADDR))
# print(getTotalComponentsRealUnitsCWBTCToken(BTCFLI_TOKEN_ADDRESS,cWBTC_ADDR))
# getNetAssetValue(getTotalComponentsRealUnitsCWBTCToken(BTCFLI_TOKEN_ADDRESS,cWBTC_ADDR),getTotalComponentsRealUnitsUSDC(BTCFLI_TOKEN_ADDRESS,UDSC_ADDR),coinGeckoPriceData(cWBTC_COINGECKO_ID))


def ETH_Supply():
    #need to update and take out funcation calls here
  return("🤖 ETH2x - $FLI BOT 🤖\nCurrent Supply "+ str(format(getCurrentSupply(ETHFLI_TOKEN_ADDRESS),',d'))+ "\nMax Supply "+ str(format(getTotalSupply(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS),',d')) + "\nCurrently at ~" +str(round((getCurrentSupply(ETHFLI_TOKEN_ADDRESS)/getTotalSupply(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)*100)))+"% of max supply\n\nLearn more about the supply cap and why it is important here: https://docs.indexcoop.com/our-products/flexible-leverage-indices/fli-technical-documentation/fli-product-parameters")

def BTC_Supply():
    #need to update and take out funcation calls here
  return("🤖 BTC2x - $FLI BOT 🤖\nCurrent Supply "+ str(format(getCurrentSupply(BTCFLI_TOKEN_ADDRESS),',d'))+ "\nMax Supply "+ str(format(getTotalSupply(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS),',d')) + "\nCurrently at ~" +str(round((getCurrentSupply(BTCFLI_TOKEN_ADDRESS)/getTotalSupply(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)*100)))+"% of max supply\n\nLearn more about the supply cap and why it is important here: https://docs.indexcoop.com/our-products/flexible-leverage-indices/fli-technical-documentation/fli-product-parameters")

def ETHmaxSupplyChange(old,new):
  return(f"🤖 The max supply cap for ETH2x - $FLI has been changed to {new:,} from {old:,}\nLearn more about the supply cap and why it is important here: https://docs.indexcoop.com/community/governance/fli-strategy-parameter-updates")

def BTCmaxSupplyChange(old,new):
  return(f"🤖 The max supply cap for BTC2x - $FLI has been changed to {new:,} from {old:,}\nLearn more about the supply cap and why it is important here: https://docs.indexcoop.com/community/governance/fli-strategy-parameter-updates")

def ETHpastRipcordTolerence():
    return("🤖 ETH2x - $FLI has fallen outside of its leverage tolerance, anyone can rebalance immediately for reward!\nSee docs here: https://docs.indexcoop.com/resources-beta/technical-overview/fli-technical-documentation/fli-keeper-bot-integration ")

def BTCpastRipcordTolerence():
    return("🤖 BTC2x - $FLI has fallen outside of its leverage tolerance, anyone can rebalance immediately for reward!\nSee docs here: https://docs.indexcoop.com/resources-beta/technical-overview/fli-technical-documentation/fli-keeper-bot-integration ")

def ETHsupplyCapWarningThreshold():
    #need to update and take out funcation calls here
  return("🤖 CAUTION! ETH2x - $FLI is at "+str(round((getCurrentSupply(ETHFLI_TOKEN_ADDRESS)/getTotalSupply(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)*100)))+"% of it’s supply cap. When Supply cap is reached there can be a disconnect from net asset value and traded value.\n Read more here: https://medium.com/indexcoop/understanding-the-eth2x-fli-premium-4ac8c5f6faa1")

def BTCsupplyCapWarningThreshold():
    #need to update and take out funcation calls here
  return("🤖 CAUTION! BTC2x - $FLI is at "+str(round((getCurrentSupply(BTCFLI_TOKEN_ADDRESS)/getTotalSupply(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)*100)))+"% of it’s supply cap. When Supply cap is reached there can be a disconnect from net asset value and traded value.\n Read more here: https://medium.com/indexcoop/understanding-the-eth2x-fli-premium-4ac8c5f6faa1")

def ETHnetAssetValueThresholdPremium(premium):
  return(f"🤖 ATTENTION! There is currently a {premium}% premium on ETH2x - $FLI compared to it’s net asset value.\nRead more here: https://medium.com/indexcoop/understanding-the-eth2x-fli-premium-4ac8c5f6faa1")
  
def BTCnetAssetValueThresholdPremium(premium):
  return(f"🤖 ATTENTION! There is currently a {premium}% premium on BTC2x - $FLI compared to it’s net asset value.\nRead more here: https://medium.com/indexcoop/understanding-the-eth2x-fli-premium-4ac8c5f6faa1")

def ETHnetAssetValueThresholdDiscount(discount):
  return(f"🤖 ATTENTION! There is currently a {discount}% discount on ETH2x - $FLI compared to it’s net asset value.\nRead more here: https://medium.com/indexcoop/understanding-the-eth2x-fli-premium-4ac8c5f6faa1")
  
def BTCnetAssetValueThresholdDiscount(premium):
  return(f"🤖 ATTENTION! There is currently a {discount}% discount on BTC2x - $FLI compared to it’s net asset value.\nRead more here: https://medium.com/indexcoop/understanding-the-eth2x-fli-premium-4ac8c5f6faa1")
