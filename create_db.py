import sqlite3

connection = sqlite3.connect('fli.db')

cursor = connection.cursor()

#create stock table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY, 
        name TEXT NOT NULL UNIQUE
    )
""")

#create stock price table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS parameters (
        id INTEGER PRIMARY KEY, 
        product_id INTEGER,
        date NOT NULL,
        maxSupply NOT NULL, 
        currentSupply NOT NULL, 
        currentLeverageRatio NOT NULL, 
        FOREIGN KEY (product_id) REFERENCES product (id)
    )
""")
connection.commit()



