import streamlit as st

st.header('Description')
st.write('AskVista is an advanced, GPT-powered tool designed to streamline daily database interactions for professionals and businesses. Leveraging the robust capabilities of the OpenAI API, this tool simplifies the complex process of data retrieval by allowing users to either upload their database or connect database directly to the tool.')

st.header('Description')

st.subheader('1. Database Compatibility')
st.write("""Users can upload their database (.sqlite only and up to a maximum of 200 MB) or just the structure of their database in various formats such as .sql, .json, or .txt. The most efficient method, however, is to connect the database directly to the tool using the code availabe at:
         
         github.com/hasnaynajmal/askvista""")

st.subheader('2. Intelligent Query Generation')
st.write("""Utilizing a structured GPT prompt system, DataQuery Assistant can generate SQL queries based on user prompts. This feature caters to a wide range of needs, whether the user requires specific data retrieval or general information about the database's structure.""")
st.subheader('3. Execution of Queries')
st.write("""If the database is uploaded or connected, the tool can not only generate but also execute SQL queries, providing real-time results directly to the user. This feature is particularly useful for users who need to interact with their data frequently and quickly.""")
st.subheader('4. Schema Retrieval and Analysis')
st.write("""Upon loading a database, DataQuery Assistant intelligently retrieves the database schema, which is then used to inform the GPT model. This ensures that the queries generated are accurate and tailored to the specific structure of the user's database.""")
st.subheader('5. Non-Execution Mode')
st.write("""For users who prefer not to upload their entire database or whose needs are limited to schema analysis, the tool provides a non-execution mode. In this mode, queries are generated based on the uploaded structure but are not executed, serving as a safe and informative way to plan database interactions.""")
st.subheader('6. Visual Generation Using Autogen')
st.write("""AskVista also supports generating auto visualisation of retrieved data using AutoGen - A Enhanced LLM's Framework by Microsoft""")
st.subheader('7. Sending Mail Using Autogen')
st.write("""AskVista also supports sending Mail of retrieved data and visuals using AutoGen.""")
