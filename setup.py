import mysql.connector
import sys
import configparser
from os import path
#from pip import main
#import subprocess

#def install(package):
#    try:
#        subprocess.check_call(
#            [sys.executable, "-m", "pip", "install", package])
#    except:
#        print("ERROR: Could not install Python Package. Check if pip3 is installed")
#        sys.exit(1)

def add_emulator(emulator, example_path,config_name):
    print("Sync "+emulator+" ? (Y/N): ", end=" ")
    choice = input()
    if choice == "y" or choice == "Y":
        while True:
            print("Enter full path to Savegame folder ("+example_path+"):", end=" ")
            path_input = input()
            if path.basename(path_input) == path.basename(example_path) and path.isdir(path_input):
                config["path"][config_name] = path_input
                break
            else:
                print("ERROR: Please enter the full path where the "+emulator+" savegames are Located ("+example_path+"). try again (Y/N): ", end=" ")
                choice = input()
                config["path"][config_name] = "none"
                if choice == "n" or choice == "N":
                    break
    else:
        config["path"][config_name] = "none"

#install("mysql-connector-python")

config = configparser.ConfigParser()
config.read("config.ini")

print("------------------------------------SETUP---------------------------------------")
print("Input your MySQL Server host: ", end=" ")
config["database"]["host"] = input()
print("Input your MySQL Server user name: ", end=" ")
config["database"]["user"] = input()
print("Input your MySQL Server password: ", end=" ")
config["database"]["password"] = input()
print("Input your MySQL Server database name: ", end=" ")
config["database"]["db"] = input()


try:
    mydb = mysql.connector.connect(
        host=config["database"]["host"],
        user=config["database"]["user"],
        password=config["database"]["password"],
        database=config["database"]["db"]
    )
    try:
        mycursor = mydb.cursor(dictionary=True, buffered=True)
        sql = "CREATE TABLE IF NOT EXISTS savegame (id INT NOT NULL AUTO_INCREMENT,filename VARCHAR(255), mtime DATETIME, file LONGBLOB, subfolder VARCHAR(255), emulator VARCHAR(255), PRIMARY KEY (id) )"
        mycursor.execute(sql)
        mydb.commit()
        print("-------------------------------MySQL DB connected-------------------------------")
        print("--------------------------------------------------------------------------------")
    except:
        print("ERROR: could not create Table")
        sys.exit(1)
except:
    print("ERROR: no connection to MySQL DB")
    sys.exit(1)


print("-----------------------------Add Savegame Locations-----------------------------")

add_emulator("Retroarch",".../Retroarch/saves","retroarch_saves")
add_emulator("Dolphin GameCube",".../Dolphin/GC","dolphin_gc_saves")
add_emulator("PCSX2",".../PCSX2/memcards","pcsx_saves")


try:
    config_file = open("config.ini", "w")
    config.write(config_file)
    config_file.close()
except:
    print("ERROR: could not write config file")
    sys.exit(1)

print("---------------------------------SETUP FINISHED--------------------------------")
