import database
object = database.DB()

def print_available_actions():    
    result = object.db_query("SELECT * FROM actions")
    for i in result:
        if not i[4]:
            print(i)

def print_assigned_actions(user_id):    
    query= "SELECT * from actions WHERE assigned_tech_id = %s"

    result = object.db_assigned_actions_query(query, user_id)

    for i in result:
        print(i)