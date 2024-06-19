import available_actions
import assign_ticket
import database

object = database.DB()
'''
Function used for actions avaiable to employees.
They can assign tickets, create tickets, see what tickets they have, mark tickets as complete
Returns: None
'''
def actions(user_id):
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
        query= "SELECT * from actions WHERE assigned_tech_id = %s"

        result = object.db_assigned_actions_query(query, user_id)

        for i in result:
            print(i)

