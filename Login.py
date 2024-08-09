# Importing the Required Libraries

import base64
import streamlit as st 
import psycopg2 as pg2
from Banking import savingsAccount
from streamlit_extras.switch_page_button import switch_page 

# Setting the Background for Login page

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

# Connecting to the Database

conn = pg2.connect(dbname="Banking", user="postgres",port = 5433,password = 'SU')
cur = conn.cursor()
st.subheader('Customer Login Page',divider ='rainbow')

# Getting the user details for login
col1,col2,col3 = st.columns([0.05,0.35,0.5])
with col2:
    st.image('thumb.jpg',width=400)
with col3:
    user1 = st.text_input('User Name:',value= None,key= 'nm2')
    pawd = st.text_input('Password:',value = None,key='pd2',type='password')
    if user1:
        user = user1.lower()
    

    try:
        cur.execute(f"select acc_no from userdetails WHERE user_name = '{user}'")
        num = cur.fetchone()
        account_num  = num[0]
        savingsAccount.autheticate(user,account_num)
    except:
        conn.rollback()
       

    button1 = st.button('Login')
    if st.button('Go to Home Page'):
        switch_page('Banking')
# Checking authentication status

    if user1 and pawd and button1:
        
            check = f"SELECT CASE WHEN EXISTS (select * from userdetails where user_name = '{user}' and password = {pawd})THEN 'TRUE' ELSE 'FALSE' END"
            cur.execute(check)
            for i in cur:
                if i[0] == 'TRUE':
                        st.success("Authentication Successful")
                        
                        # if authenticated user, the page switches to user_menu.py
                        
                        switch_page('User_menu')
                        
                else:
                    
                    st.error('Authentication Failed')
                    conn.rollback()
    else:
        st.error('kindly fill in all details')    
    


  
                    
