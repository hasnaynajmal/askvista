
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import sqlite3
from askvista.system_message.prompts import SYSTEM_MESSAGE
from sqlite3 import Error
import streamlit as st
import os
from utils.db_connection import *


#----- Handle uploaded File, if file is .db extension, it will create connection with DB to get it's schema. ------#

def handle_file_upload(uploaded_file):
    """Handle the logic for file upload and processing."""
    try:
        file_name = uploaded_file
        
        print('\n------Inside Handle File Upload\n---------')

        if file_name.endswith('.db'):

            print('\n------Uploaded File is DB \n---------')

            schemas = get_upload_schema(uploaded_file)
            message = SYSTEM_MESSAGE.format(schema=schemas)

            print('\n------We got the message \n---------')
            print(message)
            st.success("Database file loaded successfully.")
            return message
        
        elif file_name.endswith(('.sql', '.json')):

            content = read_other_content(file_name)

            if content:
                st.success('File loaded successfully.')
                return content
            else:
                st.error("Failed to load file content.")

    except Exception as e:
        st.error(f"An error occurred: {e}")


#----- Create Connection with Existing Database in Repository -------#

def use_existing_connection():
    """Handle the logic for using an existing database connection."""
    
    schemas = get_schema_representation()

    message = SYSTEM_MESSAGE.format(schema=schemas)


    st.success("No File Uploaded. Application will use existing DB.")
    return message


#---- Create Connection with Uplaoded Database -----#

def create_upload_connection(uploaded_file):
    """ Create or connect to an SQLite database """
    print('-----------------------------')
    conn = None
    try:
        
        print(f'Temporary database file created at: {uploaded_file}')
        conn = sqlite3.connect(uploaded_file)
        print('Connection Successful')
        return conn
    
    except sqlite3.Error as e:
        print(e)
        if conn:
            conn.close()
        # Optionally remove the temporary file if an error occurred
        if os.path.isfile(uploaded_file):
            os.remove(uploaded_file)



#--- Get schema of Uploaded Database File ----#

def get_upload_schema(uploaded_file):
    """ Retrieve the schema of the SQLite database. """
    print('Inside Upload Schema Function')
    try:
        conn = create_upload_connection(uploaded_file)
        cursor = conn.cursor()
        cursor.execute("SELECT type, name, sql FROM sqlite_master WHERE type='table'")

        tables = cursor.fetchall()

        db_schema = {}

        for table in tables:
            table_name = table[1]  # Correct index for the table name

            # Query to get column details for each table
            cursor.execute(f"PRAGMA table_info('{table_name}');")  # Properly quote the table name
            columns = cursor.fetchall()
        
            column_details = {}
            for column in columns:
                column_name = column[1]
                column_type = column[2]
                column_details[column_name] = column_type
        
            db_schema[table_name] = column_details

        if db_schema:
            st.success('Schema Loaded')
        else:
            st.error('Schema Empty')
        return db_schema
    except Exception as e:
        st.error('An error occurred: ' + str(e))
        print('An error occurred: ', e)


#------ Read Content of files other than .db extension, such as sql, txt, json.

def read_other_content(file_path):
    """ Read the content of a file and return it as a string. """
    print('Reading File :: ',file_path)
    encodings = ['utf-8', 'utf-16', 'iso-8859-1']  # List of encodings to try
    for encoding in encodings:
        print(encoding)
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            print(f"Failed decoding '{file_path}' with {encoding}. Trying next encoding...")
        except FileNotFoundError:
            print(f"Error: The file '{file_path}' does not exist.")
            return None
        except Exception as e:
            print(f"An error occurred while reading '{file_path}': {e}")
            return None
    st.write(f"All encodings failed. Unable to read '{file_path}'.")
    return None