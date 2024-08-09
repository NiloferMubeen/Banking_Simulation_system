# IMPORT THE REQUIRED LIBRARIES

import base64
import pandas as pd
import streamlit as st
import psycopg2 as pg2
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page

# ESTABLISHING THE DATABASE CONNECTION

conn = pg2.connect(dbname="Banking", user="postgres",port = 5433,password = 'SU')
cur = conn.cursor()

# CREATING USERDETAILS AND TRANSACTIONS TABLE

create = '''CREATE TABLE IF NOT EXISTS userdetails(
	                        user_name text UNIQUE ,
	                        password int,
                            balance int,
                            acc_no int UNIQUE,
                            PRIMARY KEY (user_name,acc_no))'''
cur.execute(create)


create_trans = f'''CREATE TABLE  if not EXISTS transactions(
                                Date DATE,
                                Account_number INT,
                                Debit TEXT ,
                                Credit TEXT,
                                debit_amount INT,
                                credit_amount INT,
                                Remarks_Bills TEXT,
                                Bill_amount INT,
                                Balance INT)'''
cur.execute(create_trans)
conn.commit()       

# CREATING SAVINGS ACCOUNT CLASS AND REQUIRED METHODS       

class SavingsAccount:
    
    # User Registration
                
    def createAccount(self,name,pwd,deposit,account):
        try:
            insert ='''INSERT INTO  userdetails(user_name,password,balance,acc_no)VALUES(%s,%s,%s,%s)'''
            data = (name,pwd,deposit,account)
            cur.execute(insert,data)
            conn.commit()
            st.markdown(f"<h5 style='text-align: center; color: #063F27;'>Account creation has been successful. Your account number is  :{account}</h5>", unsafe_allow_html=True)
            
        except:
            st.error('Registeration Unsuccessful. Username already exists')
            conn.rollback()
            
    def autheticate(self,user,account_num):
        self.user = user
        self.account_num = account_num
    
    
    # Transactions between Users   
    
    def fundtransfer(self,user,account_num,user_acc,amount):
        
        query = f'''select balance from userdetails where user_name = '{user}' and acc_no = {account_num} '''
        cur.execute(query) 
        balance = cur.fetchone()
        
        if balance[0] < amount:
            st.warning("Insufficient balance")
            
        else:
            
            # updating the debit account
            
            new_bal = balance[0] - amount
            upd_bal = f'''UPDATE userdetails SET balance = {new_bal} where acc_no = {account_num} '''
            cur.execute(upd_bal)
            conn.commit()
            self.displayBalance(account_num)
            
            #updating the credit account
            
            query2= f'''select balance from userdetails where acc_no = {user_acc}'''
            cur.execute(query2)
            bal2 = cur.fetchone()
            new_bal2 = bal2[0] + amount
            add_bal = f'''UPDATE userdetails SET balance = {new_bal2} where acc_no = {user_acc}'''
            cur.execute(add_bal)
            conn.commit()
            
            return (new_bal,new_bal2)  
        
    
    # Bill payments 
        
    def bill_payment(self,amount,account_num):
        query = f'''select balance from userdetails where acc_no = {account_num} '''
        cur.execute(query) 
        balance = cur.fetchone()
        
        if balance[0] < amount:
            st.warning("Insufficient balance")
        else:
            new_bal = balance[0] - amount
            upd_bal = f'''UPDATE userdetails SET balance = {new_bal} where acc_no = {account_num} '''
            cur.execute(upd_bal)
            conn.commit()
            self.displayBalance(account_num)
            return new_bal
    
    
    # Money Deposit(for demo purpose)
        
    def deposit(self,account_num, depositAmount):
        query3 = f'''SELECT balance from userdetails WHERE acc_no = {account_num}'''
        cur.execute(query3)
        que3 = cur.fetchone()
        user_bal = que3[0] + depositAmount
        
        query4 = f'''UPDATE userdetails SET balance = {user_bal} where acc_no ={account_num}'''
        cur.execute(query4)
        conn.commit()
        st.success("Deposit was successful.")
        self.displayBalance(account_num)
    
    
    # View Available balance   

    def displayBalance(self,account_num):
        cur.execute(f"select balance from userdetails where acc_no = {account_num}")
        bal = cur.fetchone()
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.markdown(f"<h2 style='text-align: center; color: #063F27;'>Available balance: {bal[0]} </h2>", unsafe_allow_html=True)
    
    
    # View complete statement
        
    def statement(self,account_num):
         cur.execute(f'''SELECT * FROM transactions WHERE Account_number = {account_num}''')
         tab = cur.fetchall()
         display = pd.DataFrame(tab,columns = ['Date','Account','Debit','Credit','Debit Amount','Credit Amount','Bills','Bill Amount','Available Balance'])
         st.table(display)
         
                                       
# Designing Streamlit PAGE  


st.set_page_config(page_title = 'BankingApp',layout='wide') 

# Setting the Background

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


# MAIN PAGE OPTION MENU

selected = option_menu("Main Menu", ['Home','Create Account','Login'], 
        icons=['house','cloud-arrow-up-fill','repeat'], menu_icon="menu-up", default_index=0,orientation ="horizontal",key='s1')


savingsAccount = SavingsAccount()

# User Registration

if selected == 'Home':
    
    with st.container():
        col1,col2,col3,col4 = st.columns([0.1,0.3,0.5,0.1])
        with col2:
            
            st.image('vector.jpg',width=300)
        
        with col3:
            st.write(" ")
            st.write(" ")
            st.header('Smart Banking',divider='rainbow')
            st.write('''Welcome to a new era of banking.
                    Our app offers all the standard banking operations 
                    such as creating accounts, depositing money, and 
                    viewing transaction history. But that's not all! 
                        We also provide you with personalized financial 
                            insights. These insights are designed to help 
                                you make informed financial decisions and manage your finances more efficiently.''')

if selected == 'Create Account':
     
                # On selecting 'Create Account', page switches to Register.py
                
                switch_page("Register")
                
                        
# User Login
                
if selected == 'Login':

            # On selecting 'Login', page switches to Login.py
            
            user = st.text_input('User Name:',value= None,key= 'nm2')  
            switch_page("Login")
                
            
                           
        
                
                
                                                 
                                    
                                                        
                                            
                        
                