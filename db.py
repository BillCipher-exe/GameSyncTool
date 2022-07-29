import mysql.connector
import os
import support
import sys


class DB:
    
    def __init__(self, mysql_config, path):
        try:
            self.mysql_config = mysql_config
            self.save_path = path
            self.mydb = mysql.connector.connect(
                host=mysql_config["host"],
                user=mysql_config["user"],
                password=mysql_config["password"],
                database=mysql_config["db"]
            )
            self.mycursor = self.mydb.cursor(dictionary=True, buffered=True)
        except:
            print("ERROR: no connection to the MySQL DB. check your details")
            sys.exit(1)


class Retroarch(DB):
    def check_entry_exist(self, filename):
        sql = "SELECT filename FROM retroarch WHERE filename=%s"
        val = (filename,)
        self.mycursor.execute(sql, val)
        myresult = self.mycursor.fetchone()
        if myresult is not None:
            return True
        else:
            return False

    # upload file to DB
    def put_file_db(self, filename, mtime):
        path = os.path.join(self.save_path, filename)
        print(filename, " Uploaded to DB")
        file = open(path, "rb").read()
        if self.check_entry_exist(filename):
            sql = "Update retroarch SET mtime = %s , file = %s WHERE filename = %s"
            val = (mtime, file, filename)
        else:
            sql = "INSERT INTO retroarch(filename,mtime,file) VALUES(%s,%s,%s)"
            val = (filename, mtime, file)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def get_file_db(self, id):
        sql = "SELECT filename, mtime, file FROM retroarch WHERE id = %s"
        val = (id,)
        self.mycursor.execute(sql, val)
        myresult = self.mycursor.fetchone()
        path = os.path.join(self.save_path, myresult["filename"])
        file = open(path, "wb")
        file.write(myresult["file"])
        file.close()
        support.set_file_last_modified(path, myresult["mtime"])
        print(myresult["filename"], "Downloaded from DB",
              "| with mtime: ", myresult["mtime"])

    def get_info_db(self):
        sql = "SELECT id, filename, mtime FROM retroarch"
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()
        