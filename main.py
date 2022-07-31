import db
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

retroarch = db.Retroarch(config["database"],config["path"]["retroarch_saves"], "retroarch")
dolphin_GC = db.Dolphin_GC(config["database"],config["path"]["dolphin_GC_saves"], "dolphin_GC")

retroarch.sync()
dolphin_GC.sync()