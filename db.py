import mysql.connector
from datetime import datetime
import os
import support


mydb = mysql.connector.connect(
    host="remotemysql.com",
    user="cFt9g9Qee7",
    password="KKgyM4qdL4",
    database="cFt9g9Qee7"
)
mycursor = mydb.cursor(dictionary=True, buffered=True)


def check_entry_exist(filename):
    sql = "SELECT filename FROM Retroarch WHERE filename=%s"
    val = (filename,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    if myresult is not None:
        return True
    else:
        return False


# upload file to DB
def put_file_db(path, filename, time):
    path = os.path.join(path, filename)
    print(filename, " Uploaded to DB")
    file = open(path, "rb").read()
    if check_entry_exist(filename):
        sql = "Update Retroarch SET SaveTime = %s , File = %s WHERE Retroarch.Filename = %s"
        val = (time, file, filename)
    else:
        sql = "INSERT INTO Retroarch(Filename,SaveTime,File) VALUES(%s,%s,%s)"
        val = (filename, time, file)
    mycursor.execute(sql, val)
    mydb.commit()


def get_file_db(path, id):
    sql = "SELECT Filename, SaveTime, File FROM Retroarch WHERE ID = %s"
    val = (id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    path = os.path.join(path, myresult["Filename"])
    file = open(path, "wb")
    file.write(myresult["File"])
    support.set_file_last_modified(path, myresult["SaveTime"])
    print(myresult["Filename"], "Downloaded from DB")


def get_info_db():
    sql = "SELECT ID, Filename, SaveTime FROM Retroarch"
    mycursor.execute(sql)
    return mycursor.fetchall()
