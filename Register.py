# Importing the Required libraries

import base64
import streamlit as st
from random import randint
from Banking import savingsAccount

# Setting the Background for Registration page

def get_base64_of_bin_file(bin_file):
            with open(bin_file, 'rb') as f:
                data = f.read()
            return base64.b64encode(data).decode()
        
def set_png_as_page_bg(png_file):
                bin_str = get_base64_of_bin_file(png_file)
                page_bg_img = '''
                                <style>
                                .stApp {
                                background-image: url("data:image/png;base64,%s");
                                background-size: cover;
                                }
                                </style>
                                ''' % bin_str
                                                        
                st.markdown(page_bg_img, unsafe_allow_html=True)
                return
set_png_as_page_bg('img2.png')

st.subheader('User Registration Page',divider= 'rainbow')

# Getting the user details to register

name = st.text_input("Name: ",key='nm1')
pwd = st.text_input("Password: ",key='pd1')
deposit = st.number_input("Initial deposit: ",key='dp1',min_value=15000)
account = randint(10000, 99999)  # a random account_num is generated for the user
button = st.button('Register')

if button:
        if name and pwd and deposit:
                        
            savingsAccount.createAccount(name,pwd,deposit,account)
                                               
        else:
            st.error('kindly fill in all details')