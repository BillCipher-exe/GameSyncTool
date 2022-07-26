import mysql.connector
from datetime import datetime
import os
import support
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

mydb = mysql.connector.connect(
    host=config["database"]["host"],
    user=config["database"]["user"],
    password=config["database"]["password"],
    database=config["database"]["db"]
)
mycursor = mydb.cursor(dictionary=True, buffered=True)


def check_entry_exist(filename):
    sql = "SELECT filename FROM retroarch WHERE filename=%s"
    val = (filename,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    if myresult is not None:
        return True
    else:
        return False


# upload file to DB
def put_file_db(path, filename, mtime):
    path = os.path.join(path, filename)
    print(filename, " Uploaded to DB")
    file = open(path, "rb").read()
    if check_entry_exist(filename):
        sql = "Update retroarch SET mtime = %s , file = %s WHERE filename = %s"
        val = (mtime, file, filename)
    else:
        sql = "INSERT INTO retroarch(filename,mtime,file) VALUES(%s,%s,%s)"
        val = (filename, mtime, file)
    mycursor.execute(sql, val)
    mydb.commit()


def get_file_db(path, id):
    sql = "SELECT filename, mtime, file FROM retroarch WHERE id = %s"
    val = (id,)
    mycursor.execute(sql, val)
    myresult = mycursor.fetchone()
    path = os.path.join(path, myresult["filename"])
    file = open(path, "wb")
    file.write(myresult["file"])
    support.set_file_last_modified(path, myresult["mtime"])
    print(myresult["filename"], "Downloaded from DB","| with mtime: ",myresult["mtime"])


def get_info_db():
    sql = "SELECT id, filename, mtime FROM retroarch"
    mycursor.execute(sql)
    return mycursor.fetchall()
