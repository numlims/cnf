import os
import yaml
import json
import configparser
from pathlib import Path
home = "home"
def makeload(path:str=None, root:str=None, fmt:str=None, make:str=None):
    """
    makeload reads the conf file from `path` rooted in `root`, creates if
    from `make` string it's not there, and returns it parsed from a given
    format.
    
    it keeps the root part extra so it can be set with a constant like
    `cnf.home`.
    
    if no config file was there and it was created, a `MakeCnfException` is
    thrown. 
    """
    p = cnfpath(root, path)
    if not os.path.exists(p):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as file:
            file.write(make)
            raise MakeCnfException(f"please edit {p}, then run again.")
            return None
    else:
        if fmt == "ini":
           config = configparser.ConfigParser()
           config.read(p)
           return config
        else:
            with open(p, "r") as file:
                if fmt == None:
                   return file.read()
                elif fmt == "yaml":
                   return yaml.safe_load(file)
                elif fmt == "json":
                   return json.load(file)
                else:
                   print(f"{fmt} not known.")
                   return None
def cnfpath(root, path):
    """
    cnfpath appends path to a cnf constant, root.
    """
    frompath = ""
    if root == None:
        frompath = ""
    elif root == home:
        frompath = Path.home()
    else:
        print(f"error: {root} not known. ")
    return os.path.join(frompath, path)
class MakeCnfException(Exception):
    def __init__(self, message:str):
        """
        """
        super().__init__(message)
