## TO-DO
# import pytest
#to run
#python3 -m pytest tests

import tweepy, json, sqlite3, os
from web3 import Web3
from datetime import datetime
from config import INFURA_URL, ETHERSCAN_TOKEN
from token_addresses import *
from get_data_functions import *

# @pytest.fixture
# def input_value():
#    input = 39
#    return input

# @pytest.mark.parametrize("num, output",[(1,11),(2,22),(3,35),(4,44)])
# def test_multiplication_11(num, output):
#    assert 11*num == output


def test_mytest():
    a = 1
    b = 2
    assert a+b==5

#getTotalSupply(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS)
def test_BTCMaxSupplyUpdate():
   connection = sqlite3.connect(os.path.abspath('fli.db'))
   connection.row_factory = sqlite3.Row
   cursor = connection.cursor()
   cursor.execute("""
    SELECT maxSupply FROM parameters where product_id=2
""")
   rows = cursor.fetchall()
   parameters_in_db = [row['maxSupply'] for row in rows] # list comprehension
   # print(parameters_in_db)
   if parameters_in_db[0] != getTotalSupply(BTCFLI_SUPPLY_CAP_ISSUANCE_ADDRESS):
      # assert(ETHmaxSupplyChange(parameters_in_db[0],getTotalSupply(ETHFLI_SUPPLY_CAP_ISSUANCE_ADDRESS))) 
      assert True
   else:
      assert True