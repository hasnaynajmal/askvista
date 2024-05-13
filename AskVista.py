import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from utils.file_upload import handle_file_upload,use_existing_connection, create_upload_connection, read_other_content, get_upload_schema
import json
from utils.functions import *
import tempfile
#from openai import AzureOpenAI
from system_message.prompts import ASSISTAN_MESSAGE_FOR_VIS, ASSISTAN_MESSAGE_FOR_MAIL
from io import BytesIO
from PIL import Image
from autogen import *
from utils.css import custom_css, ChangeButtonColour
from openai import OpenAI
import pandas as pd


# Function to apply custom CSS

#---------------------------------------------------------#
custom_css()
#---------------------------------------------------------#

# ------------------- Connections ----------------------- #

st.markdown('<div class="title">AskVista</div>', unsafe_allow_html=True)

st.markdown('<div class="sub-title">GPT Powered Data Operator with Autogen</div>', unsafe_allow_html=True)

#--------------------- File Upload -------------------#


uploaded_file = st.file_uploader("Upload File.\n\n Supported Formats: (.sql .json .db)",key="unique_file_uploader")


#------------------- API Inputs -------------------#

api_col, model_col = st.columns(2)

model = model_col.selectbox('Select your OpenAI Model',('Select a Model','gpt-4-1106-preview','gpt-3.5-turbo-16k','gpt-3.5-turbo','gpt-3.5-turbo-0125','gpt-3.5-turbo-1106'))

openai_api = api_col.text_input(label='Enter your OpenAI API KEY', type='password')


#----------------------Azure Integration----------------------#

# client = AzureOpenAI(
#     api_version=st.secrets["VERSION"],
#     azure_endpoint=st.secrets["ENDPOINT"],
#     api_key =  st.secrets["OPENAI_API_KEY"]
# )


#-----------------------------------------------------------------#

#----------------------AutoGen Configuration----------------------#

config_list = [{
    "model": model,  # model name
    "api_key": openai_api
}]


#----------------------AutoGen Configuration for Azure----------------------#

# config_list = [{
#     "model": st.secrets["MODEL"],
#     "api_key": st.secrets["OPENAI_API_KEY"],
#     "azure_endpoint": st.secrets["ENDPOINT"],
#     "api_type": "azure",
#     "api_version": st.secrets["VERSION"]
# }]

#-----------------------------------------------------------------#

#--------------OpenAI Client Define------------------#

client = OpenAI(api_key=openai_api)

# ----------------------------------------- #


#------------------Managing Session States--------------------#

if 'formatted_system_message' not in st.session_state:
    st.session_state['formatted_system_message'] = None

if 'temp_db_path' not in st.session_state:
    st.session_state['temp_db_path'] = None

if 'use_connection' not in st.session_state:
    st.session_state['use_connection'] = None

if 'image' not in st.session_state:
        st.session_state.image = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model


#------------ Connection Buttons -----------------#

cols = st.columns(4)

ChangeButtonColour('Load File', 'black', 'black','#FEECE2', 'white', '160px')  # For a specific width
ChangeButtonColour('Use Existing Connection', 'white', 'white','#D04848' ,'black', '200px')  # For full width


#--------------Handle File Uploads------------------#


if cols[1].button('Load File', key='b1'):
    
    if uploaded_file:

        with tempfile.NamedTemporaryFile(delete=False, suffix='.db') as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_db_path = tmp_file.name

        st.session_state['temp_db_path'] = temp_db_path

        #--- Setting the Path of Uploaded File.
        file = temp_db_path

        # Store the system message for the Uplaoded File in session state to access it outside the button execution flow
        st.session_state['formatted_system_message'] = handle_file_upload(file)

        st.session_state['use_connection'] = 1

        if st.session_state['formatted_system_message']:
            #st.success('File Loaded Successfully')
            st.success("Database Uploaded")
        
        else:
            st.error('No File Loaded Successfully, please try again.')
        
    else:
        st.error('No File Uploaded, Please upload a file first, then Load')


#------------- Use Default DB Connection --------------#


if cols[2].button('Use Existing Connection', key='b2'):

    # Store the message in session state
    st.session_state['formatted_system_message'] = use_existing_connection()
    msg = st.session_state['formatted_system_message']
    st.session_state['use_connection'] = 2


#Setting Temporary path for the uploaded file.

temp_db_path = st.session_state['temp_db_path']

#Getting System Message for GPT

system_message = st.session_state['formatted_system_message']

db_status = st.session_state['use_connection']


#------------------ Calling Autogen  ----------------#

def should_activate_autogen_visual(user_input):
    # Implement logic to check for keywords or conditions
    keywords = ["visualize", "plot", "graph","print","visualise"]
    return any(keyword in user_input.lower() for keyword in keywords)

def should_activate_autogen_mail(user_input):
    # Implement logic to check for keywords or conditions
    keywords = ["send", "email", "mail", "text", 'gmail', 'outlook']
    return any(keyword in user_input.lower() for keyword in keywords)


def call_autogen_api_visual(msg,prompt):

    try:

        data_for_autogen = pd.read_csv('./coding/data.csv')

        data_top5 = data_for_autogen.head()
        data_str = data_top5.to_string(index=False, header=True)

    except:
        data_str = 'No data Source availble, so act accordingly.'

    if os.path.exists('./coding/visual.png'):
        os.remove('./coding/visual.png')
    
    msg_for_as = ASSISTAN_MESSAGE_FOR_VIS.format(data_source = data_str)

    asst = AssistantAgent("asst", llm_config={"seed": 42, "config_list": config_list, "temperature": 0,  }, system_message=msg_for_as)

    user_proxy = UserProxyAgent("user_proxy", 
                        llm_config={"config_list": config_list}, 
                        human_input_mode="NEVER", 
                        max_consecutive_auto_reply=10,is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
                        code_execution_config={
                                                "work_dir": "coding",
                                                "use_docker": False,  
                                            },)
            
    user_proxy.initiate_chat(asst, message=prompt)

    #message_content = next((entry['content'] for entry in reversed(response.chat_history) if entry['role'] == 'assistant' and not entry['content'].startswith('exitcode')), None)

    try:
        if st.image('./coding/visual.png', caption='Autogen Generated'):
            adds = ('./coding/visual.png')
            return adds
        else:
            st.error('No visualisation/image Found')
        
    except:
        st.error('No visualisation/image Found')

def call_autogen_api_mail(msg,prompt):
    
    msg_for_as = ASSISTAN_MESSAGE_FOR_MAIL.format()

    asst = AssistantAgent("asst", llm_config={"seed": 42, "config_list": config_list, "temperature": 0,  }, system_message=msg_for_as)

    user_proxy = UserProxyAgent("user_proxy", 
                        llm_config={"config_list": config_list}, 
                        human_input_mode="NEVER", 
                        max_consecutive_auto_reply=15,is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
                        code_execution_config={
                                                "work_dir": "coding",
                                                "use_docker": False,  
                                            },)
            
    res = user_proxy.initiate_chat(asst, message=prompt)

    return res

    #message_content = next((entry['content'] for entry in reversed(response.chat_history) if entry['role'] == 'assistant' and not entry['content'].startswith('exitcode')), None)


# ----------------- Chat Interaction Code ----------------------- #

@st.experimental_fragment
def download_img(image):

    try: 
        image = Image.open(img_ad)
        buf = BytesIO()
        image.save(buf, format="PNG")
        byte_im = buf.getvalue()

        if byte_im:
            btn = st.download_button(
                label="Download Image",
                data=byte_im,
                file_name="imagename.png",
                mime="image/jpeg",
                )
        
    except:
        st.error('No visualisation was Generated, please try again.')

# ----------------- Chat Interaction Code ----------------------- #

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if system_message:

    if openai_api:

        if prompt := st.chat_input("Hi there, what's up?"):

            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            messages_to_send = [{"role": "system", "content": system_message}] + [

                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            
            ]

            msg_for_autogen = ''

            for msg in messages_to_send:

                msg_for_autogen += '\n'+ msg['role'] + ' : '+ msg['content'] +'\n'

            if should_activate_autogen_visual(prompt):

                            with st.chat_message("assistant"):
                                    st.markdown('Generating Visualisation.....')
                            
                            #------ Activate Autogen Only if the User needs any visualisation --------#
                            img_ad = call_autogen_api_visual(msg_for_autogen, prompt)
                            
                            download_img(img_ad)

                            st.session_state.messages.append({"role": "assistant", "content": 'Visualisation Generated'})

                            #st.image(img_ad, caption='Autogen Generated Visualisation')

        

            #---------Activate The Mail Function on if you are providing your mail credentials in the System Message for Mail else won't work-----#



            # elif should_activate_autogen_mail(prompt):

            #     with st.chat_message("assistant"):
            #             st.markdown('Working on it.....')
                
            #     #------ Activate Autogen Only if the User needs any visualisation --------#
            #     res = call_autogen_api_mail(msg_for_autogen, prompt)
            #     if res:
            #         with st.chat_message("assistant"):
            #             st.markdown('Email Sent!')

            #     st.session_state.messages.append({"role": "assistant", "content": 'Email Has been Written into your Draft'})

                #st.image(img_ad, caption='Autogen Generated Visualisation')
            


            else:
                with st.chat_message("assistant"):

                    #--------------Default API Integrated Response----------#
                    st.markdown('Thinking....')
                    response = client.chat.completions.create(
                        model=model,
                        messages=messages_to_send,
                    )


                    #--------------Azure API Integrated Response----------#

                    # response = client.chat.completions.create(
                    #     model="model", # engine = "deployment_name".
                    #     messages=messages_to_send
                    # )

        
                    if response and response.choices:

                    #if response :

                        # Handling response from GPT

                        #Azure API
                        #message_content = response.choices[0].message.content  # Corrected access to the message content
                        
                        
                        #Default API Response

                        message_content = response.choices[0].message.content
                        
                        
                        response = message_content

                        if response.startswith('```'):
                            data_res = handle_response(response)
                            

                            try:
                                #---- Sending Model Response to Display Function and Returning query to execute it -----#

                                query = display_on_interface(data_res)
                                
                                df = handle_execution_button(query, data_res['Query Type'], temp_db_path, db_status)


                                df.to_csv('./coding/data.csv', index=False)

                            except json.JSONDecodeError as e:
                                st.error(f"Error decoding the JSON response: {e}")

                            except KeyError as e:
                                st.error(f"Missing key in JSON response: {e}")

                            interface_message = """
                                SQL Query: {query} 
                                \nDescription: {description} 
                                \nCritical Level: {critical_level} 
                                \nQuery Type: {query_type}
                                \nData: {data}""".format(

                                query=data_res['Query'],
                                description=data_res['Description'],
                                critical_level=data_res['Critical Level'],
                                query_type=data_res['Query Type'],
                                data = df
                            )

                        else:

                            interface_message = response
                            st.write(interface_message)

                st.session_state.messages.append({"role": "assistant", "content": interface_message})
    else:
        st.write('Please Enter Valid OpenAI API Key')

else:
    st.markdown('<div class="status-message">No Connection Exists</div>', unsafe_allow_html=True)