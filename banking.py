
import streamlit as st
import psycopg2 as pg2
from random import randint
from streamlit_option_menu import option_menu

conn = pg2.connect(dbname="Banking", user="postgres",port = 5433,password = 'SU')
cur = conn.cursor()


create = '''CREATE TABLE IF NOT EXISTS userdetails(
	                        user_name text ,
	                        password varchar(8),
                            balance int,
                            acc_no int,
                            PRIMARY KEY (user_name,acc_no))'''
cur.execute(create)
conn.commit()

create_trans = f'''create table if not exists TRANSACTIONS(
                                debit_account_number int ,
                                credit account_number int,
                                Deposit_amount int,
                                Balance int)'''
cur.execute(create_trans)
                        
class SavingsAccount:
    def __init__(self):
        self.savingsAccounts = {}
        
    def createAccount(self, name,pwd, initialDeposit):
        self.accountNumber = randint(10000, 99999)
        self.savingsAccounts[self.accountNumber] = [name,pwd, initialDeposit]
        return self.accountNumber

    def authenticate(self, name,accountNumber):
        st.write(name,accountNumber)       
        check = f"select * from userdetails where user_name = '{name}' and acc_no = {accountNumber}"
        cur.execute(check)
        if cur:
                st.error("Authentication Successful")
                return True
        else:
            st.error("Authentication Failed")
            return False

    def fundtransfer(self,user,account_num,user_acc,amount):
        query = f'''select initial_deposit from userdetails where user_name = '{user}' and acc_no = {account_num} '''
        balance = cur.execute(query) 
        st.write(balance)
        if balance < amount:
            st.warning("Insufficient balance")
        else:
            # updating the debit account
            new_bal = balance - amount
            upd_bal = f'''UPDATE userdetails SET balance = {new_bal} where acc_no = {account_num} '''
            cur.execute(upd_bal)
            self.displayBalance(account_num)
            
            #updating the credit account
            query2= f'''select initial_deposit from userdetails where acc_no = {user_acc}'''
            bal2 = cur.execute(query2)
            new_bal2 = bal2 + amount
            add_bal = f'''UPDATE userdetails SET balance = {new_bal2} where acc_no = {account_num}'''
            cur.execute(add_bal)
            conn.commit()
            

    def deposit(self, depositAmount):
        
        self.savingsAccounts[self.accountNumber][1] += depositAmount
        st.success("Deposit was successful.")
        self.displayBalance()
       

    def displayBalance(self,account_num):
        bal = f'select balance from userdetails where acc_no = {account_num}'
        st.markdown(f"<h4 style='text-align: center; color: #063F27;'>Available balance: {bal} </h4>", unsafe_allow_html=True)
        
        
st.set_page_config(page_title = 'BankingApp',layout='wide') 


selected = option_menu("Main Menu", ['Home','Create Account','Login'], 
        icons=['house','cloud-arrow-up-fill','repeat'], menu_icon="menu-up", default_index=0,orientation ="horizontal")


savingsAccount = SavingsAccount()


if selected == 'Create Account':
                name = st.text_input("name: ",key='nm1')
                pwd = st.text_input("Password: ",key='pd1')
                deposit = st.number_input("Initial deposit: ",key='dp1',min_value=15000)
                account = savingsAccount.createAccount(name,pwd, deposit)
                button = st.button('Register')
                if button:
                    if name and pwd and deposit:
                        insert ='''INSERT INTO  userdetails(user_name,password,initial_deopsit,acc_no)VALUES(%s,%s,%s,%s)'''
                        data = (name,pwd,deposit,account)
                        cur.execute(insert,data)
                        conn.commit()
                        st.subheader(f"Account creation has been successful. Your account number is  :red[{account}]")
                       
                    else:
                        st.error('kindly fill in all details')
                
if selected == 'Login':
                
                user = st.text_input('User Name:',value= None,key= 'nm2')
                pawd = st.text_input('Password:',value = None,key='pd2')
                account_num = st.text_input('Account number:',value=None,key='dp2')
                
                button1 = st.button('Login')
                if button1 :
                    authenticationStatus = savingsAccount.authenticate(user,int(account_num))
                    if authenticationStatus is True:
                        while True:
                            st.write(f'Hello, {user}')
                            option = st.selectbox("Select an option",("Fund Transfer", "Deposit", "View Balance","Statement",'Logout'),index = 0)
                        
                            if option == "Fund Transfer":
                                user_acc = st.text_input('Enter the Account Number')
                                amount = st.number_input("Enter a amount")
                                button2 = st.button('Pay')
                                if button2:
                                    savingsAccount.fundtransfer(user,account_num,user_acc,amount)
                                
                            elif option == "Deposit":
                                
                                depositAmount= st.number_input("Enter an amount to be deposited")
                                savingsAccount.deposit(depositAmount)
                                
                            elif option == "View Balance":
                                savingsAccount.displayBalance()
                                
                            elif option == 'logout':
                                break
            
