import support
import db
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

retroarch = db.Retroarch(config["database"],config["path"]["retroarch_saves"])

def sync_retroarch(path):
    local_files = support.files(path)
    server_files = retroarch.get_info_db()

    outdated_local = support.list_of_outdated_saves(local_files,server_files)
    for x in outdated_local:
        retroarch.get_file_db(x["id"])
    
    outdated_server = support.list_of_outdated_saves(server_files,local_files)
    for x in outdated_server:
        retroarch.put_file_db(x["filename"], x["mtime"])


sync_retroarch(config["path"]["retroarch_saves"])
