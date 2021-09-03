import sqlite3, os
from web3 import Web3
from datetime import datetime
from config import INFURA_URL, ETHERSCAN_TOKEN
from token_addresses import *
from get_data_functions import *

connection = sqlite3.connect(os.path.abspath('fli.db'))
connection.row_factory = sqlite3.Row

cursor = connection.cursor()
# print(os.path.abspath('fli.db'))
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("current date and time -> ", dt_string) 

#create Nav table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS nav (
        id INTEGER PRIMARY KEY, 
        product_id INTEGER,
        date NOT NULL,
        calculatedNAV NOT NULL, 
        coinGeckoPrice NOT NULL, 
        NAVDiff NOT NULL, 
        FOREIGN KEY (product_id) REFERENCES product (id)
    )
""")

connection.commit()

ethNAV = getNetAssetValue(getTotalComponentsRealUnitsCETHToken(ETHFLI_TOKEN_ADDRESS,cETH_ADDR),getTotalComponentsRealUnitsUSDC(ETHFLI_TOKEN_ADDRESS,UDSC_ADDR),coinGeckoPriceData(cETH_COINGECKO_ID))
ethCoinGeckoPrice = coinGeckoPriceData(ETHFLI_COINGECKO_ID)
ethNAVDiff = round(NAVDiff(ethNAV,ethCoinGeckoPrice),2)
btcNAV = getNetAssetValue(getTotalComponentsRealUnitsCWBTCToken(BTCFLI_TOKEN_ADDRESS,cWBTC_ADDR),getTotalComponentsRealUnitsUSDC(BTCFLI_TOKEN_ADDRESS,UDSC_ADDR),coinGeckoPriceData(cWBTC_COINGECKO_ID))
btcCoinGeckoPrice = coinGeckoPriceData(BTCFLI_COINGECKO_ID)
btcNAVDiff = round(NAVDiff(btcNAV,btcCoinGeckoPrice),2)


#insert ETH2x-FLI nav
cursor.execute("INSERT INTO nav (product_id, date, calculatedNAV, coinGeckoPrice, NAVDiff) VALUES (?,?,?,?,?)",(1, dt_string, ethNAV, ethCoinGeckoPrice,ethNAVDiff))

#insert BTC2x-FLI nav
cursor.execute("INSERT INTO nav (product_id, date, calculatedNAV, coinGeckoPrice, NAVDiff) VALUES (?,?,?,?,?)",(2, dt_string, btcNAV, btcCoinGeckoPrice,btcNAVDiff))


connection.commit()