import os
import yaml
import json
import configparser
from pathlib import Path
home = "home"
def makeload(path:str, root:str=None, fmt:str=None, make:str=None):
    """
    makeload reads the conf file from `path` rooted in `root`, creates
    it using `make` as template string if it's not there, and returns it
    parsed from a given format.
    
    it keeps the root part extra so it can be set with a constant like
    `cnf.home`.
    """
    p = cnfpath(root, path)
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as file:
            file.write(make)
            print(f"cnf: please edit {p}, then run again.")
            return None
    else:
        with open(p, "r") as file:
            out = None
            if fmt == None:
               out = file.read()
            elif fmt == "yaml":
               out = yaml.safe_load(file)
            elif fmt == "json":
               out = json.load(file)
            elif fmt == "ini":
               config = configparser.ConfigParser()
               out = config.read(file)
            else:
                print(f"{fmt} not known.")
            return out
def cnfpath(root, path):
    """
    cnfpath appends path to a cnf constant, root.
    """
    frompath = ""
    if root == None:
        frompath = ""
    elif root == cnf.home:
        frompath = Path.home()
    else:
        print(f"error: {root} not known. ")
    return os.path.join(frompath, path)
