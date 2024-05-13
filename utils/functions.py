from sqlite3 import Error
import streamlit as st
import pandas as pd
import json
from AskVista import * # type: ignore
from utils.db_connection import *
from utils.file_upload import *
from sqlalchemy import create_engine

#----- Function to Query Database ----------#

def query_database(query, conn):
    print('Inside Query DB Function')
    
    """Run SQL query and return results in a dataframe"""

    return pd.read_sql_query(query, conn)

def handle_response(response):

    response = response.replace('```', '').strip()

    if response.startswith('json'):
        response = response[4:].strip()  # Remove the first four characters and any whitespace

        json_response = json.loads(response)

        query = json_response['Query']  # Make sure the key matches exactly
        description = json_response['Description']
        critical_level = json_response['Critical Level']
        query_type = json_response['Query Type']

        combined_dict = {
        "Query": query,
        "Description": description,
        "Critical Level": critical_level,
        "Query Type": query_type
        }

        check_json = True

        return combined_dict
    
    else:
        text_ans = response
        return text_ans

## ---------------------------------- ##
# ---------- Data To Display -------- ##

def display_on_interface(data):
    
    st.subheader("SQL Query")
    st.code(data['Query'], language="sql")

    st.subheader("Description")
    st.write(data['Description'])

    st.subheader("Critical Level")
    st.write(data['Critical Level'])

    st.subheader("Query Type")
    st.write(data['Query Type'])

    query = data['Query']

    return query


def query_upload_database(get_query,conn):
    print('Inside Query DB Function')
    
    """Run SQL query and return results in a dataframe"""

    return pd.read_sql_query(get_query, conn)


def execute_upload_sql_command(sql_command, conn):
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


def execute_query(get_query, get_query_type, uploaded_file, db_status):

    print('Uploaded file we got inside execute query function :: ',uploaded_file)

    if db_status==1:
    
        file_name = uploaded_file
        

        if file_name.endswith(('.db')):
            
            conn = create_upload_connection(uploaded_file)

            if get_query_type.lower()=='display':
                sql_results = query_upload_database(get_query, conn)
                #sql_results.to_csv('../coding/data.csv')
                st.subheader("Query Results:")
                st.dataframe(sql_results)
                return sql_results

            # --------------- At moment, No function supported other than Data Display -------- #
        
            #elif get_query_type.lower()=='insert':
            #    execute_upload_sql_command(get_query,conn)
            #    st.write('Inside Executing Uploaded DB. No write permission accepted.')
                
            else:
                st.error('No operation other than Insertion or Display supported.')

        if file_name.endswith(('.sql', '.json')):
            st.write('Query Execution Not Supported on uploaded file. Either the file is not .db or this type of query is not supported.')

    elif db_status==2:

        conn = create_connection()
        
        #---- Only if the query type is of Data retrieval, the application will execute it. ----#
        if get_query_type.lower()=='display':

            sql_results = query_upload_database(get_query, conn)
            
            # st.write(sql_results)
            # sql_results.to_csv('../coding/results.csv')
            
            st.subheader("Query Results:")
            st.dataframe(sql_results)
            return sql_results

        # --------------- At moment, No function supported other than Data Display -------- #

        # elif get_query_type.lower()=='insert':
        #    execute_sql_command(get_query,conn)
        #    st.write('Query Executed Successfully.')

        else:
            st.error('No operation other than Insertion or Display supported.')
    else:
        st.error('No DB Exists')


if "visibility" not in st.session_state:
    st.session_state.visibility = "collapsed"

@st.experimental_fragment # Just add the decorator
def handle_execution_button(query, query_type, uploaded_file, db_status):

    # This function is triggered when the Exection button is clicked

    
    ##--------------- Adding Button As A Check if User wants to execute Query or Not ------------------##
    
    #if st.button('Execute Query'):

        try:

            # Run the SQL query and display the results
            return execute_query(query, query_type, uploaded_file, db_status)


            ##-----------Option To Edit the query before Executing --------------##

            #st.chat_input(key='exec-a',placeholder=query)

        except Exception as e:
            st.error(f"An error occurred: {e}") 

    

    # elif st.button('Edit Query'):
    #     try:
    #         edit_query(query, query_type, uploaded_file, db_status)

    #     except Exception as e:
    #         st.error(f"An error occurred: {e}") 
    
    # elif st.button('No'):
    #     None


# if 'sql_results' not in st.session_state:
#     st.session_state['sql_results'] = None

# @st.experimental_fragment # Just add the decorator
# def edit_query(query, query_type,uploaded_file,db_status):
#     qc = st.text_input(label='Edit Your Query ',label_visibility=st.session_state.visibility,value=query)
#     print('Query here :: ',qc)
#     if st.button('Execute Now'):
#         try:
#             print('Inside execute now button :: ')
#             sql_results = execute_query(qc, query_type, uploaded_file, db_status)
#             st.session_state['sql_results'] = sql_results
#             print('Inside session state :: ',sql_results)

#         except Exception as e:
#             st.error(f"An error occurred: {e}") 
    
#     st.subheader('Returned Edited')
#     results = st.session_state['sql_results']
#     print(results)
#     st.dataframe(results)