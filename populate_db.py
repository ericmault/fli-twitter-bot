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

products = ["ETH2x-FLI","BTC2x-FLI"]


cursor.execute("""
    SELECT name FROM products
""")

rows = cursor.fetchall()
products_in_db = [row['name'] for row in rows] # list comprehension
print(products_in_db)

# cursor.execute("""
#     SELECT maxSupply FROM parameters where product_id = 1
# """)

# rows = cursor.fetchall()
# parameters_in_db = [row['maxSupply'] for row in rows] # list comprehension
# print(parameters_in_db)


for i in products:
    try:
        if i not in products_in_db:
            print(f"Added new product")
            cursor.execute("INSERT INTO products (name) VALUES (?)",(i,))
    except Exception as e:
        print(i)
        print(e)
    
connection.commit()


#insert ETH2x-FLI parameters
cursor.execute("INSERT INTO parameters (product_id, date, maxSupply, currentSupply, currentLeverageRatio) VALUES (?,?,?,?,?)",(1, dt_string,getTotalSupply(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS),getCurrentSupply(ETHFLI_TOKEN_ADDRESS),getCurrentLeverageRatio(ETHFLI_STRATEGY_ADAPTER_ADDRESS)))

#insert BTC2x-FLI parameters
cursor.execute("INSERT INTO parameters (product_id, date, maxSupply, currentSupply, currentLeverageRatio) VALUES (?,?,?,?,?)",(2, dt_string,getTotalSupply(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS),getCurrentSupply(BTCFLI_TOKEN_ADDRESS),getCurrentLeverageRatio(BTCFLI_STRATEGY_ADAPTER_ADDRESS)))


connection.commit()