import mysql.connector
import subprocess
import sys
import configparser

from pip import main


def install(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    except:
        print("ERROR: Could not install Python Package. Check if pip3 is installed")
        sys.exit(1)
install("mysql-connector-python")

config = configparser.ConfigParser()
config.read("config.ini")

print("----------------------------SETUP-------------------------------")
print("Input your MySQL Server host: ",end=" ")
config["database"]["host"] = input()
print("Input your MySQL Server user name: ",end=" ")
config["database"]["user"] = input()
print("Input your MySQL Server password: ",end=" ")
config["database"]["password"] = input()
print("Input your MySQL Server database name: ",end=" ")
config["database"]["db"] = input()

try:
    config_file = open("config.ini","w")
    config.write(config_file)
    config_file.close()
except:
    print("ERROR: could not write config file")
    sys.exit(1)
try:
    mydb = mysql.connector.connect(
        host=config["database"]["host"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        database=config["database"]["db"]
    )
    try:
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        add_retroarch = "CREATE TABLE IF NOT EXISTS retroarch (id INT NOT NULL AUTO_INCREMENT,filename VARCHAR(255), mtime DATETIME, file LONGBLOB, subfolder VARCHAR(255), PRIMARY KEY (id) )"
        add_dolphin = "CREATE TABLE IF NOT EXISTS dolphin (id INT NOT NULL AUTO_INCREMENT,filename VARCHAR(255), mtime DATETIME, file LONGBLOB, subfolder VARCHAR(255), PRIMARY KEY (id) )"
        mycursor.execute(add_retroarch)
        mycursor.execute(add_dolphin)
        mydb.commit()
        print("----------------------------SETUP COMPLETE----------------------------")
        print("run main.py to sync your games")
        print("----------------------------------------------------------------------")
    except:
        print("ERROR: could not create Table")
        sys.exit(1)
except:
    print("ERROR: no connection to MySQL DB")
    sys.exit(1)

