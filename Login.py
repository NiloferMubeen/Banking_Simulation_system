import base64
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
set_png_as_page_bg('img3.png')


conn = pg2.connect(dbname="Banking", user="postgres",port = 5433,password = 'SU')
cur = conn.cursor()
st.subheader('Customer Login Page',divider ='rainbow')

user = st.text_input('User Name:',value= None,key= 'nm2')
pawd = st.text_input('Password:',value = None,key='pd2')
account_num = st.text_input('Account number:',value=None,key='dp2')

button1 = st.button('Login')

if button1:
    check = f"SELECT CASE WHEN EXISTS (select * from userdetails where acc_no = {account_num})THEN 'TRUE' ELSE 'FALSE' END"
    cur.execute(check)
    for i in cur:
        if i[0] == 'TRUE':
                st.error("Authentication Successful")
        else:
            st.error('Authentication failed')
        
    
st.divider()    
                     
option = option_menu("User Menu", ["Fund Transfer","Pay bills","Deposit", "View Balance","Statement",'Logout'], 
    icons=['house','cloud-arrow-up-fill','repeat'], menu_icon="menu-up", default_index=0,orientation ="vertical",key='op2')

                                         
                                                    
if option == "Fund Transfer":
            try:
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
            except:
                st.error('Please Login')                                 
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
                st.error('Please Login')                                                                                                                                                                             
                                                                                                                                                                
elif option == "Deposit":
            try:                                                                                                                                                    
                                depositAmount= st.number_input("Enter an amount to be deposited")
                                button3 = st.button('Deposit')
                                if button3 :
                                    savingsAccount.deposit(account_num,depositAmount)
            except:
                st.error('Please Login')                                                                                                                                                         
elif option == "View Balance":
            try: 
                            savingsAccount.displayBalance(account_num)
            except:
                st.error('Please Login')                                                                                                                                                            
elif option == "Statement":
            try:
                        savingsAccount.statement(account_num)
            except:
                st.error('Please Login')
                
elif option == 'Logout':
                switch_page('Banking')
             
                     
