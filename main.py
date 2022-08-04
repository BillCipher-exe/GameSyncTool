import db
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

if config["path"]["retroarch_saves"] != "none":
    exceptions = ["/Users/", ]
    retroarch = db.DB(
        config["database"], config["path"]["retroarch_saves"], "retroarch",exceptions)
    retroarch.sync()

if config["path"]["dolphin_gc_saves"] != "none":
    exceptions = ["/", ]
    dolphin_GC = db.DB(
        config["database"], config["path"]["dolphin_gc_saves"], "dolphin_GC",exceptions)
    dolphin_GC.sync()

if config["path"]["pcsx_saves"] != "none":
    exceptions = ["/", ]
    pcsx2 = db.DB(
        config["database"], config["path"]["pcsx_saves"], "pcsx2",exceptions)
    pcsx2.sync()

