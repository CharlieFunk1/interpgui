from app import db
from app.models import Strip, Configure
import os
import json
from app.json_rw import write_json, read_json

SAVE_FOLDER = "./config_saves/"

def save_config(config_name):
    if config_name != None:
        path = (SAVE_FOLDER + config_name)
        isFile = os.path.isfile(path)
        if isFile == False:
            os.mkdir(path)
        write_json(SAVE_FOLDER + config_name + "/")
        

def query_saves():
    saves = os.listdir(SAVE_FOLDER)
    return saves

def load_config(config_name):
    read_json(SAVE_FOLDER, config_name)
