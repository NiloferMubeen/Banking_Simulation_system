import streamlit as st 
import psycopg2 as pg2
from Banking import savingsAccount
from streamlit_option_menu import option_menu  
from streamlit_extras.switch_page_button import switch_page 

conn = pg2.connect(dbname="Banking", user="postgres",port = 5433,password = 'SU')
cur = conn.cursor()

user = st.text_input('User Name:',value= None,key= 'nm2')
account_num = st.text_input('Account number:',value=None,key='dp2')



                                                             
option = option_menu("User Menu", ["Fund Transfer", "Deposit", "View Balance","Statement",'Logout'], 
            icons=['house','cloud-arrow-up-fill','repeat'], menu_icon="menu-up", default_index=0,orientation ="vertical",key='op2')

        #option = st.selectbox("Select an option",("Fund Transfer", "Deposit", "View Balance","Statement",'Logout'),index = None,key='xyz1')
            
           
            
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

elif option == 'Logout':
       switch_page('Banking')
                                         
        