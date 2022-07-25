from os import listdir
from os.path import isfile, join
from datetime import datetime
import os
import db


# get list of files at path
def files(mypath):
    items = []
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in onlyfiles:
        date_t = get_mtime(join(mypath, i))
        entry = {"filename": i, "mtime": date_t}
        items.append(entry)
    return items


#set mtime 
def set_file_last_modified(file_path, time):
    dt_epoch = time.timestamp()
    os.utime(file_path, (dt_epoch, dt_epoch))


#get mtime
def get_mtime(path):
    mtime = os.path.getmtime(path)
    date_t = datetime.fromtimestamp(mtime)
    return date_t.replace(microsecond=0)


# get list of dict with all savegames newer on the server and non existant localy
def get_newer_on_server(local_path):
    newer_on_server = []
    local_files = files(local_path)
    server_files = db.get_info_db()
    for server in server_files:
        found = False
        for x in range(len(local_files)):
            if server["filename"] == local_files[x]["filename"]:
                found = True
                break
        if(found == True):
            #print(server["filename"], "found localy")
            if server["mtime"] > local_files[x]["mtime"]:
                print("file in DB ", server["mtime"],
                      "is newer than Local file Time", local_files[x]["mtime"])
                newer_on_server.append(server)
            elif server["mtime"] == local_files[x]["mtime"]:
                print(server["filename"], " Is up to Date")
            else:
                print("file in DB ", server["mtime"],
                      "is older than Local file Time", local_files[x]["mtime"])
        else:
            print(server["filename"], "not found localy")
            newer_on_server.append(server)
    print("files newer in DB: ", newer_on_server)
    return newer_on_server


# get list of dict with all savegames newer on the local and non existant on server
def get_newer_on_local(local_path):
    newer_on_local = []
    local_files = files(local_path)
    server_files = db.get_info_db()
    for local in local_files:
        found = False
        for x in range(len(server_files)):
            if local["filename"] == server_files[x]["filename"]:
                found = True
                break
        if(found == True):
            #print(local["filename"], "found on server")
            if local["mtime"] > server_files[x]["mtime"]:
                print("file on local ", local["mtime"],
                      "is newer file in DB", server_files[x]["mtime"])
                newer_on_local.append(local)
            elif local["time"] == server_files[x]["mtime"]:
                print(local["filename"], "Is up to Date")
            else:
                print("file on local ", local["mtime"],
                      "is older than file DB", server_files[x]["mtime"])
        else:
            print(local["filename"], "not found on Server")
            newer_on_local.append(local)
    print("files newer on local: ", newer_on_local)
    return newer_on_local
