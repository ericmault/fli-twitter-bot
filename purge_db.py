import sqlite3
connection = sqlite3.connect('fli.db')
cursor = connection.cursor()

# Delete Data
cursor.execute("DELETE FROM products")
connection.commit()

# Delete Data
cursor.execute("DELETE FROM parameters")
connection.commit()

# Drop table
# cursor.execute("DROP TABLE products")
# connection.commit()


# Drop table
# cursor.execute("DROP TABLE parameters")
# connection.commit()


