import db
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

if config["path"]["retroarch_saves"] != "none":
    retroarch = db.Retroarch(config["database"],config["path"]["retroarch_saves"], "retroarch")
    retroarch.sync()

if config["path"]["dolphin_gc_saves"] != "none":
    dolphin_GC = db.Dolphin_GC(config["database"],config["path"]["dolphin_gc_saves"], "dolphin_GC")
    dolphin_GC.sync()