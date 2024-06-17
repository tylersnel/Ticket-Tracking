import create_user
import user_signin
import available_actions
import assign_ticket


user_choice=input("Press N for new user or S to sign in ")
user_choice=user_choice.lower()
while user_choice!='n' and user_choice!='s':
    user_choice=input("Incorrect input. Press N for new user or S to sign in ") 
    user_choice=user_choice.lower()

if user_choice=='n':
    create_user.create_user()

if user_choice=='s':
    #user_id so it can be used in other functions without have to query the db again for id
    user_id=user_signin.signin()
    

print("What would you like to do?")
user_action=input("Press A for available actions or Q to see your action queue ")
user_action=user_action.lower()
while user_action!='a' and user_action!='q':
    user_action=input("Incorrect input. Press N for new user or S to sign in ") 
    user_action=user_action.lower()

if user_action=='a':
    available_actions.print_available_actions()
    action_choice=input("Enter number of action you would like to assign to yourself or press B to go back ")
    if action_choice.lower()!="b":
        assign_ticket.assign_ticket(user_id, action_choice)

if user_action=='q':
    pass