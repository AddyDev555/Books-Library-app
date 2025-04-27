import pandas as pd
import sqlite3

# Load Excel data into a DataFrame
excel_file = 'sheet.xlsx'
df = pd.read_excel(excel_file)

# Connect to SQLite database (creates the database file if it doesn't exist)
db_file = 'database.db'
conn = sqlite3.connect(db_file)

# Specify the table name and write the DataFrame to the database
table_name = 'Busdata'
df.to_sql(table_name, conn, index=False, if_exists='replace')

# Commit and close the connection
conn.commit()
conn.close()
