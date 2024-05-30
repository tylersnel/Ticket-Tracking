import database

def print_available_actions():
    object = database.DB()
    result = object.db_query("SELECT * FROM actions")
    for i in result:
        if not i[4]:
            print(i)