import streamlit as st
from random import randint
from Banking import savingsAccount

st.subheader('User Registration Page',divider= 'rainbow')

name = st.text_input("name: ",key='nm1')
pwd = st.text_input("Password: ",key='pd1')
deposit = st.number_input("Initial deposit: ",key='dp1',min_value=15000)
account = randint(10000, 99999)
button = st.button('Register')
if button:
        if name and pwd and deposit:
                        
            savingsAccount.createAccount(name,pwd,deposit,account)
                                               
        else:
            st.error('kindly fill in all details')