# sql_db.py
import sqlite3
from sqlite3 import Error
from datetime import date, timedelta
from tqdm import tqdm
import pandas as pd

#DATABASE_NAME = "./database/chinook.db"

DATABASE_NAME = 'sqlite-sakila.db'

def create_connection():
    """ Create or connect to an SQLite database """
    conn = None;

    try:
        conn = sqlite3.connect(DATABASE_NAME)
    except Error as e:
        print(e)
    return conn

def execute_sql_command(sql_command, conn):
    """Execute an SQL command that does not return a DataFrame."""
    #conn = create_connection()  # Ensure connection is established
    try:
        c = conn.cursor()
        c.execute(sql_command)  # Execute the SQL command
        conn.commit()  # Commit the transaction
        print("Command executed successfully")
    except Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()  # Ensure connection is closed


def query_database(query):
    """ Run SQL query and return results in a dataframe """
    conn = create_connection()
    print('Printing the query db')
    df = pd.read_sql_query(query, conn)
    print('Printing DF:',df)
    conn.close()
    return df


def get_schema_representation():
    """ Get the database schema in a JSON-like format """

    conn = create_connection()
    cursor = conn.cursor()

    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    db_schema = {}
    
    for table in tables:
        table_name = table[0]
        
        # Query to get column details for each table
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        column_details = {}
        for column in columns:
            column_name = column[1]
            column_type = column[2]
            column_details[column_name] = column_type
        
        db_schema[table_name] = column_details
    
    conn.close()

    print('Schema accuqired')

    return db_schema


# # This will create the table and insert 100 rows when you run sql_db.py
# if __name__ == "__main__":

#     # Querying the database
#     # print(query_database("SELECT * FROM albums"))

#     # Getting the schema representation
#     print(get_schema_representation())