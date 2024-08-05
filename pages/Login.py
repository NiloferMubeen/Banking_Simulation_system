import streamlit as st 
from Banking import savingsAccount
from streamlit_extras.switch_page_button import switch_page

st.subheader('User Login Page',divider= 'rainbow')


user = st.text_input('User Name:',value= None,key= 'nm2')
pawd = st.text_input('Password:',value = None,key='pd2')
account_num = st.text_input('Account number:',value=None,key='dp2')
                
button1 = st.button('Login')
if user and pawd and account_num and button1:
    
            authenticationStatus = savingsAccount.authenticate(user,int(account_num))

            if authenticationStatus == True:
                     
                    switch_page('user_menu')   
                                                                  
                        
            else:
                st.error("Authentication Failed")
else:
                    
    st.warning('Kindly fill in all details')