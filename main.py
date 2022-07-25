import support
import db
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

print(config["path"]["retroarch_saves"])

def sync_retroarch(path):
    local_update_list = support.get_newer_on_server(path)
    for x in local_update_list:
        db.get_file_db(path, x["id"])
    server_update_list = support.get_newer_on_local(path)
    for x in server_update_list:
        db.put_file_db(path, x["filename"], x["mtime"])


sync_retroarch(config["path"]["retroarch_saves"])

#input("Press enter to exit ;)")
