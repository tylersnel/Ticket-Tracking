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
    print("What would you like to do?")
    user_action=input("Press I to input a new ticket, S to check status of your open actions, E to edit ticket ")
    user_action=user_action.lower()
    while user_action!='i' and user_action!='s' and user_action!='e':
        user_action=input("Incorrect input. Press I to input a new ticket, S to check status of your open actions, E to edit ticket ") 
        user_action=user_action.lower()

    if user_action == 'i':
        input_ticket.create_ticket(customer_id)