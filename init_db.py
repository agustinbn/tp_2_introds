import mysql.connector

with open("prode.sql") as f:
    sql = f.read()

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="prode"
)

cursor = db.cursor()

for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        db.commit()

cursor.close()
db.close()