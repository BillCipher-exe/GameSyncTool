import mysql.connector
import subprocess
import sys
import configparser
from pip import main
from os import path


def install(package):
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", package])
    except:
        print("ERROR: Could not install Python Package. Check if pip3 is installed")
        sys.exit(1)


install("mysql-connector-python")

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

print("Sync Retroarch? (Y/N): ", end=" ")
choice = input()
if choice == "y" or choice == "Y":
    while True:
        print("Enter full path to Savegame folder (.../Retroarch/saves):", end=" ")
        retroarch_path = input()
        if path.basename(retroarch_path) == "saves" and path.isdir(retroarch_path):
            config["path"]["retroarch_saves"] = retroarch_path
            break
        else:
            print("ERROR: Please enter the full path where the Retroarch savegames are Located (.../Retroarch/saves). try again (Y/N): ", end=" ")
            choice = input()
            config["path"]["retroarch_saves"] = "none"
            if choice == "n" or choice == "N":
                break
else:
    config["path"]["retroarch_saves"] = "none"

print("Sync Dolphin (GameCube)? (Y/N): ", end=" ")
choice = input()
if choice == "y" or choice == "Y":
    while True:
        print("Enter full path to Savegame folder (.../Dolphin Emulator/GC):", end=" ")
        dolpin_gc_path = input()
        if path.basename(dolpin_gc_path) == "GC" and path.isdir(dolpin_gc_path):
            config["path"]["dolphin_GC_saves"] = dolpin_gc_path
            break
        else:
            print("ERROR: Please enter the full path where the Dolphin GC savegames are Located (.../Dolphin Emulator/GC). try again (Y/N): ", end=" ")
            config["path"]["dolphin_GC_saves"] = "none"
            choice = input()
            if choice == "n" or choice == "N":
                break
else:
    config["path"]["dolphin_GC_saves"] = "none"


try:
    config_file = open("config.ini", "w")
    config.write(config_file)
    config_file.close()
except:
    print("ERROR: could not write config file")
    sys.exit(1)

print("---------------------------------SETUP FINISHED--------------------------------")
