import mysql.connector
import os
import support
import sys


class DB:
    
    def __init__(self, mysql_config, path, table):
        try:
            self.mysql_config = mysql_config
            self.save_path = path
            self.table = table
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

    def check_entry_exist(self, filename, subfolder):
        sql = "SELECT filename FROM " + self.table + " WHERE filename=%s AND subfolder = %s"
        val = (filename, subfolder)
        self.mycursor.execute(sql, val)
        myresult = self.mycursor.fetchone()
        if myresult is not None:
            return True
        else:
            return False

    def put_file_db(self, filename, mtime, subfolder):
        path = path = self.save_path + subfolder + filename
        print(filename, " Uploaded to DB")
        file = open(path, "rb").read()
        if self.check_entry_exist(filename, subfolder):
            sql = "Update " + self.table + " SET mtime = %s , file = %s, subfolder = %s WHERE filename = %s AND subfolder = %s"
            val = (mtime, file, subfolder, filename, subfolder)
        else:
            sql = "INSERT INTO " + self.table + " (filename,mtime,file, subfolder) VALUES(%s,%s,%s,%s)"
            val = (filename, mtime,file ,subfolder)
        self.mycursor.execute(sql, val)
        self.mydb.commit()

    def get_file_db(self, id, subfolder):
        sql = "SELECT filename, mtime, file, subfolder FROM " + self.table + " WHERE id = %s AND subfolder = %s"
        val = (id,subfolder)
        self.mycursor.execute(sql, val)
        myresult = self.mycursor.fetchone()
        path = self.save_path + myresult["subfolder"] + myresult["filename"]
        if not os.path.isdir(self.save_path + myresult["subfolder"]):
            os.makedirs(self.save_path + myresult["subfolder"])
        file = open(path, "wb")
        file.write(myresult["file"])
        file.close()
        support.set_file_last_modified(path, myresult["mtime"])
        print(myresult["filename"], "Downloaded from DB",
              "| with mtime: ", myresult["mtime"])

    def get_info_db(self):
        sql = 'SELECT id, filename, mtime, subfolder FROM ' + self.table
        self.mycursor.execute(sql)
        return self.mycursor.fetchall()


class Retroarch(DB):
    def sync_retroarch(self):
        local_files = support.get_files(self.save_path)
        server_files = self.get_info_db()

        outdated_local = support.list_of_outdated_saves(local_files,server_files)
        for x in outdated_local:
            self.get_file_db(x["id"], x["subfolder"])
        
        outdated_server = support.list_of_outdated_saves(server_files,local_files)
        for x in outdated_server:
            self.put_file_db(x["filename"], x["mtime"], x["subfolder"])
        