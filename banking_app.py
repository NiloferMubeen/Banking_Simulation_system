# IMPORTING ALL THE NECESSARY LIBRARIES

import base64
import pickle
import random
import streamlit as st
import psycopg2 as pg2
import streamlit_authenticator as stauth
from streamlit_option_menu import option_menu

# SET PAGE CONFIGURATION

st.set_page_config(page_title = 'Banking_app',layout='wide') 

# LOGIN PAGE BACKGROUND

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

set_png_as_page_bg('img1.png')

# CONNECTING TO DATABASE

conn = pg2.connect(dbname="Banking", user="postgres",port = 5433,password = 'SU')
curr = conn.cursor()

create = '''CREATE TABLE IF NOT EXISTS userdetails(
	user_name text,
	password varchar(8),
        acc_no bigint,
     )'''
     
curr.execute(create)
conn.commit()

# USER LOGIN CREDENTIALS
pwd_list = ['abc','def']
hashed_passwords = stauth.Hasher(pwd_list).generate()

# with open('hashed.pkl','wb') as file:
       # pickle.dump(hashed_passwords,file)
       
with open('hashed.pkl','rb') as file:
        hashed_passwords = pickle.load(file)

    
credentials = {
        "usernames":{
                        'nilomubeen':{"name":'Nilofer',"password":hashed_passwords[0]},
                        'shaik':{"name":'Abdur Razack',"password":hashed_passwords[1]}
                     }
                }


# USER VALIDATION

a1,a2 = st.columns(2)

       

with a2:
                button1 = st.button('SignUp')
                if button1:
                        name = st.text_input('Enter the name',value=None)
                        name1 = st.text_input("Enter the UserName",value=None)
                        pwd = st.text_input('Enter Password',value=None)
                        user_id = random.randint(100000,999999)
                        
                button = st.button('Register')
                if name1 not in credentials.keys():
                                credentials['usernames'][name1] = dict(name=name,password= pwd)
                                pwd_list.append(pwd)
                else:
                                st.error('Username Already Exists !')
                        
                user_dic = { 'user':[],
                                'pwd': [],
                                'acc_no': []}
                        
                        
                        
                if name1 and pwd and user_id:
                                user_dic['user'].append(name1)
                                user_dic['pwd'].append(pwd)
                                user_dic['acc_no'].append(user_id)
                        if button:
                                        
                        
                authenticator = stauth.Authenticate(credentials,'Banking','abcdef',cookie_expiry_days = 30)
                name,authentication_status,username = authenticator.login('main')
                
                      
                if authentication_status == False:
                        st.error("Username/Password is Incorrect!")

                if authentication_status == None:
                        st.error("Please Enter your UserName and Password",icon="⚠️")

if authentication_status:
        
        # USER PAGE BACKGROUND
        
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
        with st.sidebar:
                selected = option_menu("Main Menu", ['Home','Accounts','Funds Transfer'], 
                                    icons=['house','cloud-arrow-up-fill','repeat'], menu_icon="menu-up", default_index=0,orientation ="vertical")
                authenticator.logout("logout","sidebar")
        
        if selected == 'Home':
                    st.subheader(f"Welcome {name}!")
                    
                    