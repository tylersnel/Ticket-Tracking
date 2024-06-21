import create_user
import user_signin
import employee_actions
import customer_actions


user_choice=input("Press N for new user or S to sign in ")
user_choice=user_choice.lower()
while user_choice!='n' and user_choice!='s':
    user_choice=input("Incorrect input. Press N for new user or S to sign in ") 
    user_choice=user_choice.lower()

if user_choice=='n':
    array=create_user.create_user()
    user_id=array[0]
    user_permissions=array[1]

if user_choice=='s':
    array=user_signin.signin()
    user_id=array[0]
    user_permissions=array[1]

if user_permissions==2:
   employee_actions.actions(user_id)

if user_permissions==1:
    customer_actions.customer_actions(user_id)