import streamlit as st

# Display the main header for the application.
st.title('AskVista: GPT Powered Data Operator')

# Provide a brief description of the application.
st.write('''
AskVista is an advanced tool that simplifies database queries and interactions using the power of GPT and OpenAI API. 
Whether you want to directly connect your database or just upload its schema, AskMatic is designed to provide you with 
the insights and answers you need.
''')

# Section for Connecting DB Through the Code.
st.header('1. Connect Your Database Directly')
st.write('''
- To connect your database directly to the code, clone the GitHub repository: [hasnaynajmal/askvista](https://github.com/hasnaynajmal/askvista).
- Navigate to the cloned directory in a Python-integrated terminal and run \n\n     `pip install -r requirements.txt` to install the required packages.
- Place your database file in the same directory or specify the path of your database.
- Open the `db_connection.py` file and set the `DATABASE_NAME` variable to the name or path of your database file.
- Execute `streamlit run AskMatic.py` in the terminal to start the application on localhost.
- On the application interface, enter your OpenAI API key and select the desired OpenAI model.
- Click on 'Use Existing Connection' to initiate the connection. You can now interact with the application via chat.
''')

# Section for Uploading DB or Schema.
st.header('2. Upload Your Database or Schema/Structure')
st.write('''
- Visit the application at [askvista.streamlit.app](https://askvista.streamlit.app).
- Drag and drop your database (max 200 mb) or schema file in the provided area or click 'Browse files' to upload from your device. Supported formats are .sql, .json, .db.
- Enter your OpenAI API key in the provided field.
- Select the OpenAI model you wish to use from the dropdown menu.
- Click on 'Load File' to upload your database schema and start the application.
- Once the application is running, you can enter your prompts to get responses from the model.
''')

# Section for Uploading DB or Schema.
st.header('''3. Use AskVista's Autogen to Send Mails''')
st.write('''
- Using AutoGen to send mails is only supported on the localhost at the moment.
- To Enable sending mails, go to the `system_message folder` in `AskVista` repository, and open `prompts.py`.
- In the `ASSISTAN_MESSAGE_FOR_MAIL`, set the following variables \n\n  `sender_email = "your-mail"` \n\n   `sender_password = "your-password"`  
\n\n    `server = smtplib.SMTP('smtp.office365.com', port)
- After that, go to main file of `AskVista.py` and activate the `if` check of `autogen mail` on line `315`.
- Now run your `AskVista.py` file in terminal using `streamlit run AskVista.py`.
''')