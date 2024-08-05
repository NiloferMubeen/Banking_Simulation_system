# IMPORT THE REQUIRED LIBRARIES
import base64
import pandas as pd
import streamlit as st
import psycopg2 as pg2
from random import randint
from streamlit_option_menu import option_menu

# ESTABLISHING THE DATABASE CONNECTION

conn = pg2.connect(dbname="Banking", user="postgres",port = 5433,password = 'SU')
cur = conn.cursor()

# CREATING USERDETAILS AND TRANSACTIONS TABLE

create = '''CREATE TABLE IF NOT EXISTS userdetails(
	                        user_name text UNIQUE ,
	                        password varchar(8),
                            balance int,
                            acc_no int UNIQUE,
                            PRIMARY KEY (user_name,acc_no))'''
cur.execute(create)


create_trans = f'''CREATE TABLE  if not EXISTS transactions(
                                Date DATE,
                                Account_number INT,
                                debit_account_number INT ,
                                credit_account_number INT,
                                debit_amount INT,
                                credit_amount INT,
                                Balance INT)'''
cur.execute(create_trans)
conn.commit()       

# REATING SAVINGS ACCOUMT CLASS AND REQUIRED METHODS       

class SavingsAccount:
            
    def createAccount(self, name,pwd,deposit,account):
        try:
            insert ='''INSERT INTO  userdetails(user_name,password,balance,acc_no)VALUES(%s,%s,%s,%s)'''
            data = (name,pwd,deposit,account)
            cur.execute(insert,data)
            conn.commit()
            st.subheader(f"Account creation has been successful. Your account number is  :red[{account}]")
        except:
            st.error('Registeration Unsuccessful. Username already exists')
        

    def authenticate(self, name,accountNumber):
          
        check = f"SELECT CASE WHEN EXISTS (select * from userdetails where user_name = '{name}' and acc_no = {accountNumber})THEN 'TRUE' ELSE 'FALSE' END"
        cur.execute(check)
        for i in cur:
            if i[0] == 'TRUE':
                st.error("Authentication Successful")
                return True
            else:
                st.error("Authentication Failed")
                return False

    def fundtransfer(self,user,account_num,user_acc,amount):
        query = f'''select balance from userdetails where user_name = '{user}' and acc_no = {account_num} '''
        cur.execute(query) 
        balance = cur.fetchone()[0]
        
        if balance < amount:
            st.warning("Insufficient balance")
        else:
            # updating the debit account
            
            new_bal = balance - amount
            st.write(new_bal)
            upd_bal = f'''UPDATE userdetails SET balance = {new_bal} where acc_no = {account_num} '''
            cur.execute(upd_bal)
            conn.commit()
            self.displayBalance(account_num)
            
            #updating the credit account
            
            query2= f'''select balance from userdetails where acc_no = {user_acc}'''
            cur.execute(query2)
            bal2 = cur.fetchone()[0]
            new_bal2 = bal2 + amount
            st.write(new_bal2)
            add_bal = f'''UPDATE userdetails SET balance = {new_bal2} where acc_no = {user_acc}'''
            cur.execute(add_bal)
            conn.commit()
        return (new_bal,new_bal2)   

    def deposit(self,account_num, depositAmount):
        query3 = f'''SELECT balance from userdetails WHERE acc_no = {account_num}'''
        cur.execute(query3)
        que3 = cur.fetchone[0]
        user_bal = que3 + depositAmount
        
        query4 = f'''UPDATE userdetails SET balance = {user_bal} where acc_no ={account_num}'''
        cur.execute(query4)
        conn.commit()
        st.success("Deposit was successful.")
        self.displayBalance(account_num)
       

    def displayBalance(self,account_num):
        cur.execute(f'select balance from userdetails where acc_no = {account_num}')
        bal = cur.fetchone()
        st.markdown(f"<h4 style='text-align: center; color: #063F27;'>Available balance: {bal[0]} </h4>", unsafe_allow_html=True)
        
    def statement(self,account_num):
         cur.execute(f'''SELECT * FROM transactions WHERE Account_number = {account_num}''')
         tab = cur.fetchall()
         display = pd.DataFrame(tab,columns = ['Date','Account','Debit Account number','Credit Account Number','Debit Amount','Credit Amount','Available Balance'])
         st.table(display)
         
                                       
# Streamlit PAGE


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

if selected == 'Create Account':
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
                        
# User Login
                
if selected == 'Login':
                
                user = st.text_input('User Name:',value= None,key= 'nm2')
                pawd = st.text_input('Password:',value = None,key='pd2')
                account_num = st.text_input('Account number:',value=None,key='dp2')
                
                button1 = st.button('Login')
                if button1 :
                        authenticationStatus = savingsAccount.authenticate(user,int(account_num))
                        st.write(f'Hello, {user}')
                while True:
                            
                           c1,c2 = st.columns(2)
                           
                           with c1:         
                                        
                                #option = option_menu("User Menu", ["Fund Transfer", "Deposit", "View Balance","Statement",'Logout'], 
                                    #icons=['house','cloud-arrow-up-fill','repeat'], menu_icon="menu-up", default_index=0,orientation ="vertical",key='op2')

                                option = st.selectbox("Select an option",("Fund Transfer", "Deposit", "View Balance","Statement",'Logout'),index = None,key='xyz1')
                           with c2:        
                                    if option == "Fund Transfer":
                                            user_acc = st.text_input('Enter the Account Number')
                                            amount = st.number_input("Enter a amount")
                                            day = st.date_input('Date')
                                            button2 = st.button('Pay')
                                            if button2:
                                                
                                                available_balance = savingsAccount.fundtransfer(user,account_num,user_acc,amount)
                                                
                                                #updating the transactions table(debit details)
                                                
                                                insert1 = '''INSERT INTO transactions(Date,Account_number,debit_account_number,debit_amount,Balance)\
                                                        VALUES(%s,%s,%s,%s,%s)'''
                                                debit = (day,account_num,user_acc,amount,available_balance[0])
                                                
                                                cur.execute(insert1,debit)
                                                conn.commit()
                                                
                                                
                                                # updating the transactions table(credit details)
                                                
                                                insert2 = '''INSERT INTO transactions(Date,Account_number,credit_account_number,credit_amount,Balance)\
                                                        VALUES(%s,%s,%s,%s,%s)'''
                                                        
                                                credit = (day,user_acc,account_num,amount,available_balance[1])
                                                
                                                cur.execute(insert2,credit)
                                                
                                                conn.commit()
                                                
                                                
                                    elif option == "Deposit":
                                            
                                            depositAmount= st.number_input("Enter an amount to be deposited")
                                            button3 = st.button('Deposit')
                                            if button3 :
                                                savingsAccount.deposit(account_num,depositAmount)
                                                
                                                
                                            
                                    elif option == "View Balance":
                                            savingsAccount.displayBalance(account_num)
                                            
                                            
                                    
                                    elif option == "Statement":
                                            savingsAccount.statement(account_num)
                                            
                                            
                                            
                                    elif option == 'logout':
                                      break