import database
object = database.DB()

def print_available_actions():    
    result = object.db_query("SELECT * FROM actions")
    for i in result:
        if not i[4]:
            print(i)

def print_assigned_actions(user_id):
    action_status='complete'    
    query= "SELECT * from actions WHERE assigned_tech_id = %s AND action_status !=%s"
    #using the db_signin in fuction so not to have duplicate queries
    result = object.db_signin(query, user_id, action_status)

    for i in result:
        print(i)