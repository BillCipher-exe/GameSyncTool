from os import listdir
from os.path import isfile, join
from datetime import datetime
import os



# get list ot file_path without subfolder
def files(mypath):
    items = []
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for i in onlyfiles:
        date_t = get_mtime(join(mypath, i))
        entry = {"filename": i, "mtime": date_t}
        items.append(entry)
    return items

#get list of file_path with subfolder
def get_path_list(rootdir, path_list=[]):
    for it in os.scandir(rootdir):
        if it.is_dir():
             get_path_list(it, path_list)
        elif it.is_file():
            path_list.append(it.path)
    return path_list

#get dict {filename, mtime, subfolder} of all files from rootdir with subfolder
def get_files(rootdir):
    rootdir = rootdir.replace("\\",'/')
    file_list = get_path_list(rootdir,[])
    files = []
    for path in file_list:
        path =  path.replace("\\",'/')
        filename = os.path.basename(path)
        subfolder = path.replace(rootdir,"")
        subfolder = subfolder.replace(filename,"")
        _dict = {"filename":filename,"mtime":get_mtime(path),"subfolder":subfolder}
        files.append(_dict)
    return files

#set mtime 
def set_file_last_modified(file_path, time):
    dt_epoch = time.timestamp()
    os.utime(file_path, (dt_epoch, dt_epoch))


#get mtime
def get_mtime(path):
    mtime = os.path.getmtime(path)
    date_t = datetime.fromtimestamp(mtime)
    return date_t.replace(microsecond=0)


#compare list of savesgames from source1 to source2 (local storage / Database)
#return list of savegames which are outdated at source 1 
def list_of_outdated_saves(source1, source2):
    outdated = []
    for _source2 in source2:
        found = False
        for x in range(len(source1)):
            if _source2["filename"] == source1[x]["filename"]:
                found = True
                break
        if(found == True):
            if _source2["mtime"] > source1[x]["mtime"]:
                print("savegame from Source2 ", _source2["mtime"],
                      "is newer than file from Source1", source1[x]["mtime"])
                outdated.append(_source2)
            elif _source2["mtime"] == source1[x]["mtime"]:
                print(_source2["filename"], "Is up to Date")
            else:
                print("savegame from source 2 ", _source2["mtime"],
                      "is older than from source 1", source1[x]["mtime"])
        else:
            print(_source2["filename"], " savegame not found in Source 1")
            outdated.append(_source2)
    #print("outdatet savegames in source 1: ", outdated)
    return outdated