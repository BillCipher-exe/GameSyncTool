import support
import db


local_update_list = support.get_newer_on_server(
    r"C:\Users\hakan\Desktop\Programming\synctool_python\test")
for x in local_update_list:
    db.get_file_db(
        r"C:\Users\hakan\Desktop\Programming\synctool_python\test", x["id"])


server_update_list = support.get_newer_on_local(
    r"C:\Users\hakan\Desktop\Programming\synctool_python\test")
for x in server_update_list:
    db.put_file_db(
        r"C:\Users\hakan\Desktop\Programming\synctool_python\test", x["filename"], x["mtime"])


#input("Press enter to exit ;)")
