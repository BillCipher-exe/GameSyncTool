from re import sub
import support
import db
import configparser
import pathlib

config = configparser.ConfigParser()
config.read("config.ini")

retroarch = db.Retroarch(config["database"],config["path"]["retroarch_saves"])

def sync_retroarch():
    local_files = support.files(retroarch.save_path)
    server_files = retroarch.get_info_db()

    outdated_local = support.list_of_outdated_saves(local_files,server_files)
    for x in outdated_local:
        retroarch.get_file_db(x["id"])
    
    outdated_server = support.list_of_outdated_saves(server_files,local_files)
    for x in outdated_server:
        retroarch.put_file_db(x["filename"], x["mtime"])

def sync_dolphin():
    save_paths = support.listdirs(config["path"]["dolphin_saves"],2)
    #print(save_paths)
    subfolder = []
    local_files =[]
    for path in save_paths:
        p = pathlib.PurePath(path)
        p_len = len(p.parts)
        item = {"region":p.parts[p_len-2],"mem_card":p.parts[p_len-1]}
        subfolder.append(item)
        local_files.append(support.files(path))

    for idx, local_f in enumerate(local_files):
        for item in local_f:
            item.update({"region": subfolder[idx]["region"], "mem_card":subfolder[idx]["mem_card"]})

    #local_files[0][0].update({"region": subfolder[0]["region"], "mem_card":subfolder[0]["mem_card"]})
    print(local_files[1])
    

        


#sync_dolphin()
sync_retroarch()
