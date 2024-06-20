import print_actions
import ticket_manager
import database

object = database.DB()
'''
Function used for actions avaiable to employees.
They can assign tickets, create tickets, see what tickets they have, mark tickets as complete
Returns: None
'''
def actions(user_id):
    print("What would you like to do?")
    user_action=input("Press A for available actions, Q to see your action queue, C to change action status ")
    user_action=user_action.lower()
    while user_action!='a' and user_action!='q' and user_action!='c':
        user_action=input("Incorrect input. Press N for new user or S to sign in ") 
        user_action=user_action.lower()

    if user_action=='a':
        print_actions.print_available_actions()
        action_choice=input("Enter number of action you would like to assign to yourself or press B to go back ")
        if action_choice.lower()!="b":
            ticket_manager.assign_ticket(user_id, action_choice)

    if user_action=='q':
        print_actions.print_assigned_actions(user_id)
    
    if user_action=='c':
        print_actions.print_assigned_actions(user_id)
        action_id=input("Enter action ID you would like to change ")
        action_status=input("Enter action status ")
        ticket_manager.change_status(action_id, action_status)

actions(13)