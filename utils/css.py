import streamlit as st
import streamlit.components.v1 as components

border = 'rgb(250,250,250,.2)' #dark mode

def custom_css():
    
    st.markdown("""
        <style>
            /* Tune the padding and margins around the buttons and the message */

            /* Adjust the message (status bar) styling */
            .status-message {
                margin-top: -80px;  /* Reduce space above the status message if needed */
                background-color: #FA9884;  /* The background color of the status message */
                color: white;  /* The text color of the status message */
                padding: 10px;  /* The padding inside the status message */
                border-radius: 5px;  /* Rounded corners for the status message */
                text-align: center;  /* Center the text inside the status message */
            }
                
            .title{
                text-align:center;
                font-family: "Source Sans Pro", sans-serif;
                font-weight: 700;
                color: rgb(250, 250, 250);
                padding: 1.25rem 0px 1rem;
                margin: 0px;
                font-size: 50px;
                line-height: 1.2
            }
                
            .sub-title{
                text-align:center;
                font-family: "Source Sans Pro", sans-serif;
                font-weight: 700;
                color: rgb(250, 250, 250);
                padding: 1rem 0px 4rem;
                margin: 0px;
                font-size: 20px;
                line-height: 0.1
            }
        </style>
    """, unsafe_allow_html=True)

def ChangeButtonColour(widget_label, font_color, hover_color,background_h_color, background_color='transparent', width='auto'):
    htmlstr = f"""
        <script>
            var elements = window.parent.document.querySelectorAll('button');

            for (var i = 0; i < elements.length; ++i) {{ 
                if (elements[i].innerText == '{widget_label}') {{ 
                    elements[i].style.color ='{font_color}';
                    elements[i].style.background = '{background_color}';
                    elements[i].style.width = '{width}';  // Set the width here

                    elements[i].onmouseover = function() {{ 
                        this.style.color = '{hover_color}';
                        this.style.borderColor = 'transparent';
                        this.style.background = '{background_h_color}';
                    }};

                    elements[i].onmouseout = function() {{ 
                        this.style.color = '{font_color}';
                        this.style.borderColor = '{border}';
                        this.style.background = '{background_color}';
                        
                    }};
                    elements[i].onfocus = function() {{
                        this.style.boxShadow = '{hover_color} 0px 0px 0px 0px';
                        this.style.borderColor = '{hover_color}';
                        this.style.color = '{hover_color}';
                        this.style.background = '{background_color}';
                    }};
                    elements[i].onblur = function() {{
                        this.style.boxShadow = 'none';
                        this.style.borderColor = '{border}';
                        this.style.color = '{font_color}';
                        this.style.background = '{background_color}';
                        
                    }};
                }}
            }}
        </script>
        """
    components.html(htmlstr, height=0, width=0)  # Using the Streamlit Components API to inject HTML

