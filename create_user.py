import database
object = database.DB()
result = object.db_query("SELECT * FROM Employees")
for i in result:
    print(i)