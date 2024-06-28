import print_actions
import ticket_manager
import database
import input_ticket

object = database.DB()

'''
File is for handling customer actions since they do not have the same permissions as employees.
They will be able to do some of what employees can do but not all. Available actions include inputting
tickets, check status of their tickets, and edit their tickets, check past tickets. Maybe get email when action is complete??
'''
def customer_actions(customer_id):
    logout=False
    while not logout:
        print("What would you like to do?")
        user_action=input("Press I to input a new ticket, S to check status of your open actions, E to edit ticket, L to logout ")
        user_action=user_action.lower()
        while user_action!='i' and user_action!='s' and user_action!='l':
            user_action=input("Incorrect input. Press I to input a new ticket, S to check status of your open actions, E to edit ticket ") 
            user_action=user_action.lower()

        if user_action == 'i':
            input_ticket.create_ticket(customer_id)

        if user_action == 's':
            #using the db_signin in fuction so not to have duplicate queries
            action_status='complete'
            query = "SELECT * FROM actions WHERE action_creator = %s AND action_status != %s" 
            result = object.db_signin(query, customer_id, action_status)

            for i in result:
                print(i)

        if user_action == 'l':
            logout=True
            print("You are logged out.")