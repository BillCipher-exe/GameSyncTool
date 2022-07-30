import db
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

retroarch = db.Retroarch(config["database"],config["path"]["retroarch_saves"], "retroarch")
dolphin = db.dolphin(config["database"],config["path"]["dolphin_saves"], "dolphin")

retroarch.sync()
dolphin.sync()