import base64
import pandas as pd
import streamlit as st 
import psycopg2 as pg2
from Banking import savingsAccount
from streamlit_option_menu import option_menu  
from streamlit_extras.switch_page_button import switch_page 


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


conn = pg2.connect(dbname="Banking", user="postgres",port = 5433,password = 'SU')
cur = conn.cursor()
st.subheader('Customer Login Page',divider ='rainbow')

user = st.text_input('User Name:',value= None,key= 'nm2')
pawd = st.text_input('Password:',value = None,key='pd2',type='password')

try:
    cur.execute(f"select acc_no from userdetails WHERE user_name = '{user}'")
    num = cur.fetchone()
    account_num  = num[0]
except:
    pass

button1 = st.button('Login')

if user and pawd and button1:
    
        check = f"SELECT CASE WHEN EXISTS (select * from userdetails where user_name = '{user}' and password = {pawd})THEN 'TRUE' ELSE 'FALSE' END"
        cur.execute(check)
        for i in cur:
            if i[0] == 'TRUE':
                    st.success("Authentication Successful")
            else:
                st.error('Authentication failed')
else:
    st.error('kindly fill in all details')    
    
st.divider() 
st.divider()
if button1 :   
    st.markdown(f"<h3 style='text-align: center; color: #063F27;'>Hello, {user} </h3>", unsafe_allow_html=True) 
    with st.container():
        col1,col2,col3 = st.columns([0.2,0.6,0.2])
        with col2:
            st.markdown(f"<h4 style='text-align: center; color: #063F27;'>Your Account Number: {account_num} </h4>", unsafe_allow_html=True)                
option = option_menu("User Menu", ["View Balance","Statement(Analysis)","Fund Transfer","Pay bills","Deposit",'Logout'], 
    icons=['house','cloud-arrow-up-fill','repeat'], menu_icon="menu-up", default_index=0,orientation ="vertical",key='op2')

                                      

if option == "Fund Transfer":
        try:                         
             user_acc = st.text_input('Enter the Account Number')
             amount = st.number_input("Enter a amount")
             day = st.date_input('Date')
             if user_acc:
                cur.execute(f'''select user_name from userdetails where acc_no = {user_acc}''') 
                paid1 = cur.fetchone()
                paid = paid1[0]   
                if paid:
                    st.write(f'Pay {paid} ?') 
                                                              
                button2 = st.button('Pay')
                                        
                if button2:
                                                                                                                                                                                    
                        available_balance = savingsAccount.fundtransfer(user,account_num,user_acc,amount)
                                                                                                                                                                                            
                        #updating the transactions table(debit details)
                                                                                                                                                                                            
                        insert1 = '''INSERT INTO transactions(Date,Account_number,Debit,debit_amount,Balance)\
                                                                                                                                                                                                    VALUES(%s,%s,%s,%s,%s)'''
                        debit = (day,account_num,paid,amount,available_balance[0])
                                                                                                                                                                                            
                        cur.execute(insert1,debit)
                        conn.commit()
                                                                                                                                                                                            
                                                                                                                                                                                            
                        # updating the transactions table(credit details)
                                                                                                                                                                                            
                        insert2 = '''INSERT INTO transactions(Date,Account_number,Credit,credit_amount,Balance)\
                                                                                                        VALUES(%s,%s,%s,%s,%s)'''
                                                                                                                                                                                                    
                        credit = (day,user_acc,user,amount,available_balance[1])
                                                                                                                                                                                            
                        cur.execute(insert2,credit)
                                                                                                                                                                                            
                        conn.commit()
                        st.success("Transaction successful")
        except:
            st.error('Account number does not exist')  
            conn.rollback()
                                                    
elif option == 'Pay bills':  
        try:                                                            
                pay = st.selectbox("Select an option",("Electricity", "Mobile Recharge", "Internet","Gas","Renew subscription","Loans","others"),index = None,key='xyz1')  
                amount = st.number_input("Enter a amount to be paid")
                day = st.date_input('Date')
                button4 = st.button('Pay Bill')
                                                                                        
                if button4:
                    available_balance = savingsAccount.bill_payment(amount,account_num)
                                                                                            
                    insert = '''INSERT INTO transactions(Date,Account_number,Remarks_Bills,Bill_amount,Balance)\
                                                                                                        VALUES(%s,%s,%s,%s,%s)'''
                    bill = (day,account_num,str(pay),amount,available_balance)
                                                                                                                                                                                                            
                    cur.execute(insert,bill)
                    conn.commit()
        except:
            st.error('Kindly Login')
            conn.rollback()                                                                                                                                                                                            
                                                                                                                                                                            
elif option == "Deposit":
        try:                                                                                                                                                                
                depositAmount= st.number_input("Enter an amount to be deposited")
                button3 = st.button('Deposit')
                if button3 :
                        savingsAccount.deposit(account_num,depositAmount)
        except:
            st.error('Kindly Login')
            conn.rollback()                                                                                                                                                                           
elif option == "View Balance":
        try:                
                    savingsAccount.displayBalance(account_num)
        except:
            st.error('Kindly Login')
            conn.rollback()                                                                                                                                                                           
elif option == "Statement(Analysis)":
        choice = st.selectbox("Queries:",
                        ("None",
                        "1. Credit Transactions History",
                        "2. Debit Transactions History", 
                        "3. Bill Payments History",
                        "4. Total Credits",
                        "5. Total Debits",
                        "6. Highest Bill",
                        "7. Highest debit Transactions",
                        "8. Highest Credit Transactions",
                        "9. Last 5 Transactions",
                        "10. Complete Statement"),
                        index=None,
                        placeholder="Select a query...")
        
        if choice == "1. Credit Transactions History":
            cur.execute(f'''SELECT Date,credit as source_account, credit_amount from transactions
                            where account_number = {account_num} and credit_amount is not null''')
            tab = cur.fetchall()
            df = pd.DataFrame(tab,columns=['Date','Source_account','Credit Amount'])
            st.table(df)
            
            
        elif choice == "2. Debit Transactions History":
            cur.execute(f'''SELECT Date,debit as source_account, debit_amount from transactions
                            where account_number = {account_num} and debit_amount is not null''')
            tab = cur.fetchall()
            df = pd.DataFrame(tab,columns=['Date','Debit_account','Debit Amount'])
            st.table(df)
            
            
        elif choice == "3. Bill Payments History":
            cur.execute(f'''SELECT Date,remarks_bills, bill_amount from transactions
                            where account_number = {account_num} and bill_amount is not null''')
            tab = cur.fetchall()
            df = pd.DataFrame(tab,columns=['Date','Remarks','Bill Amount'])
            st.table(df)
            
            
        elif choice == "4. Total Credits":
            cur.execute(f'''select sum(credit_amount) from transactions where account_number = {account_num}''')
            tab = cur.fetchone()
            st.markdown(f"<h4 style='text-align: center; color: brown;'>Total Credit amount : {tab[0]} </h4>", unsafe_allow_html=True)
        
        
        elif choice == "5. Total Debits":
            cur.execute(f'''select sum(debit_amount) from transactions where account_number = {account_num}''')
            tab = cur.fetchone()
            st.markdown(f"<h4 style='text-align: center; color: brown;'>Total Debit amount : Rs.{tab[0]} </h4>", unsafe_allow_html=True)
        
        
        elif choice == "6. Highest Bill":
            cur.execute(f'''SELECT remarks_bills, sum(bill_amount) from transactions
                            where account_number = {account_num} and bill_amount is not null
                            GROUP BY remarks_bills
                            order by sum(bill_amount) desc
                            limit 1''')
            tab = cur.fetchall()
            st.markdown(f"<h4 style='text-align: center; color: brown;'>You have paid {tab[0][0]} bill of Rs.{tab[0][1]} </h4>", unsafe_allow_html=True)
        
        
        elif choice == "7. Highest debit Transactions":
            cur.execute(f'''SELECT debit, sum(debit_amount) as total from transactions
                            where account_number = {account_num} and debit is not null
                            group by debit
                            order by total desc
                            limit 1''')   
            tab = cur.fetchall()
            st.markdown(f"<h4 style='text-align: center; color: brown;'>Highest number of debit transactions have been made to: {tab[0][0]}</h4>", unsafe_allow_html=True) 
            st.markdown(f"<h4 style='text-align: center; color: brown;'>Total amount : Rs.{tab[0][1]} </h4>", unsafe_allow_html=True) 
        
        
        elif choice == "8. Highest Credit Transactions":
            cur.execute(f'''SELECT credit, sum(credit_amount) as total from transactions
                            where account_number = {account_num} and credit is not null
                            group by credit
                            order by total desc
                            limit 1''')   
            tab = cur.fetchall()
            st.markdown(f"<h4 style='text-align: center; color: brown;'>Highest number of Credit transactions have been made to: {tab[0][0]}</h4>", unsafe_allow_html=True) 
            st.markdown(f"<h4 style='text-align: center; color: brown;'>Total amount : Rs.{tab[0][1]} </h4>", unsafe_allow_html=True) 
        
        
        
        elif choice == "9. Last 5 Transactions":
            cur.execute(f'''select * from transactions where account_number = {account_num}
                            order by date desc
                            limit 5''')
            tab = cur.fetchall()
            df = pd.DataFrame(tab,columns = ['Date','Account','Debit','Credit','Debit Amount','Credit Amount','Bills','Bill Amount','Available Balance'])
            st.table(df)
        
        
        elif choice == "10. Complete Statement":
            try:                
                        savingsAccount.statement(account_num)
            except:
                st.error('Kindly Login')
                conn.rollback()                   
                            
elif option == 'Logout':
                    switch_page('Banking')
                        
                                
