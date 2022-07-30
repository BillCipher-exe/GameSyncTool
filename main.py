import db
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

retroarch = db.Retroarch(config["database"],config["path"]["retroarch_saves"], "retroarch")

retroarch.sync_retroarch()
