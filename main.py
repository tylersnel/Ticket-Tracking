import create_user
import user_signin


user_choice=input("Press N for new user or S to sign in ")
user_choice=user_choice.lower()
while user_choice!='n' and user_choice!='s':
    user_choice=input("Incorrect input. Press N for new user or S to sign in ") 
    user_choice=user_choice.lower()

if user_choice=='n':
    create_user.create_user()

if user_choice=='s':
    user_signin.signin()