import database
object = database.DB()

''' Used for searching old and current tickets.
    Useful for seeing how many tickets someone has submitted or
    how many actions a certain employee has done, etc
'''

def search():
    print("Enter search parameter or press enter to skip parameter")
    unit_name = input("Search by unit name or press enter to skip: ")
    action_type = input("Search by action type or press enter to skip: ")
    sm_last_name = input("Search by SM's last name or press enter to skip: ")
    assigned_tech_id = input("Search by Tech ID or press enter to skip: ")
    action_status = input("Search by action status or press enter to skip: ")
    action_creator = input("Search by action creator or press enter to skip: ")

    query = "SELECT * FROM actions WHERE unit_name=%s OR action_type=%s OR sm_last_name=%s OR assigned_tech_id=%s OR action_status=%s OR action_creator=%s"

    result= object.db_search(query, unit_name, action_type, sm_last_name, assigned_tech_id, action_status, action_creator)

    if result:
            for i in result:
                print(i)
    else:
            print('Error')
