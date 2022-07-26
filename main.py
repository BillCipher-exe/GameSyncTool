import support
import db
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def sync_retroarch(path):
    local_files = support.files(path)
    server_files = db.get_info_db()

    outdated_local = support.list_of_outdated_saves(local_files,server_files)
    for x in outdated_local:
        db.get_file_db(path, x["id"])
    
    outdated_server = support.list_of_outdated_saves(server_files,local_files)
    for x in outdated_server:
        db.put_file_db(path, x["filename"], x["mtime"])


sync_retroarch(config["path"]["retroarch_saves"])



