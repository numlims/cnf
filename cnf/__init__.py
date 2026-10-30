# __init__.py was generated from init.ct. 
# if you edit __init__.py, run `ct -tc __init__.py` afterwards to update init.ct.
# when editing this file leave the `` tags.
#``ct version 0.1.1
#``ct files init.ct __init__.py

# # cnf
# 
# cnf creates and loads configuration files.  1``//__init__.py:
# imports for makeload.  8``/import:
import os
# imports for cnfpath.  16``/import
from pathlib import Path
# imports for _load.  22``/import
import yaml
import json
import configparser
#``8
# the root constants.  7``/const:
home = "home"  # in the user's home directory
system = "system"  # system wide
#``7
# makeload reads the conf file(s) at `path` rooted in cnf.home,
# cnf.system or both and parses them from a given format, subsequent
# values overwriting values before.
# 
# if no config file is there it creates one at the first writable root from `make`.
# 
# `company` is needed for the windows config paths.
# 
# if no config file was there and it was created, a `MakeCnfException` is
# thrown.   2``/makeload:
def makeload(path:str=None, roots:str=None, company:str=None, fmt:str=None, make:str=None):
    # resolve the complete paths.  3.``
    paths = []
    for root in roots:
        paths.append(_cnfpath(root, path, company=company))
    # try to load files at the resoled paths.  keep track of whether at any
    # of the paths there is an actual file.  4``
    anyexists = False
    mergedcontent = {}
    for p in paths:
        exists, content = _load(p, fmt)
        if exists:
            anyexists = True
        _overwrite(mergedcontent, content)
    # if there isn't a file at any of the paths, create one from
    # make-template at the first writeable path.  5``
    if not anyexists:
        anywriteable = False
        for p in paths:
            if os.access(p, os.W_OK):
                anywriteable = True
                _make(p, make)
                raise MakeCnfException(f"stub config file created at {p}. please edit.")
                return None
        if not anywriteable:
            raise Exception(f"cnf: none of the config paths {paths} was writable, please try to put a config file there manually using this template: {make}")  # TODO should this be a MakeCnfException?  or another custom exception?
            return None
    # return whatever content was loaded (and merged) from the one or more
    # roots.  6``
    return mergedcontent
    #``3
#``2
# _cnfpath appends path to root, which can be cnf.home or cnf.system.
# company is needed for the windows config paths.  9``/_cnfpath:
def _cnfpath(root, path, company=None):
    # in windows both local and system wide config paths need a company
    # name, so give an error if no company specified.  10``_:
    if company is None:
        raise Exception(f"cnf: company needs to be specified for windows config paths.")
    # get the root constant.  11``
    rootpath = ""
    if root == None:
        rootpath = ""
    elif root == home:
        # the home location of conf files is ~/.config/ for posix and USERPROFILE/AppData/Local/<company>/ for windows.
        # 
        # for windows, see https://learn.microsoft.com/en-us/archive/blogs/patricka/where-should-i-store-my-data-and-configuration-files-if-i-target-multiple-os-versions  12``./home:
        if os.name == "posix":
            rootpath = os.path.join(Path.home(), ".config/")
        elif os.name == "nt":
            rootpath = os.path.join(Path.home(), f"AppData/Local/{company}")
        else:
            raise Exception(f"cnf: no home config location for os {os.name}.")
        #``12
    elif root == system:
        # the system-wide location of conf files is /etc/ for posix and C:\ProgramData\<company>\<app> for windows.  13``../system:
        if os.name == "posix":
            rootpath = os.path.join("/etc/")
        elif os.name == "nt":
            rootpath = os.path.join(f"/ProgramData/{company}/")
        else:
            raise Exception(f"cnf: no system-wide config location for os {os.name}.")
        #``13
    # else say the root is not known.  14``/_cnfpath/_
    else:
        raise Exception(f"cnf: root {root} not known.")
    # append the path given by the user.  15``
    return os.path.join(rootpath, path)
    #``10
#``9
# make creates a stub config file at path p.  17``/_make:
def _make(p:str, content:str):
    if os.path.exists(p):
        raise Exception(f"cnf: file exists at {p}, not overwriting it.")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as file:
        file.write(content)
#``17
# _load loads the config file at path, parsing it as fmt.  18``/_load:
def _load(p:str, fmt:str):
    # from the returned content can't be inferred whether the file exists (an empty yaml file parses as None, not as an empty dict), so return whether the file exists.  19``_:
    exists = os.path.exists
    # configparser doesn't need an opened file, it reads a path.  20``
    if fmt == "ini":
       config = configparser.ConfigParser()
       config.read(p)
       return exists, config
    # read the other formats from opened file.  21``
    else:
        with open(p, "r") as file:
            if fmt == None:
               return exists, file.read()
            elif fmt == "yaml":
               return exists, yaml.safe_load(file)
            elif fmt == "json":
               return exists, json.load(file)
            else:
               print(f"{fmt} not known.")
               return exists, None
    #``19
#``18
# _overwrite overwrites the values in dicta with what's in dictb.  23``/_overwrite:
def _overwrite(dicta=None, dictb=None):
    # do nothing if dictb is None.  24``_:
    if dictb is None:
        return
    # go over the keys in dict b.  25``
    for key in dictb:
        # key is not in dicta: just put it in.  26.``
        if not key in dicta:
            dicta[key] = dictb[key]
        # dictb at key is a map: recurse.  27``
        elif isinstance(dictb[key], dict):
            overwrite(dicta[key], dictb[key])
        # dictb at key is not a map: overwrite.  28``
        else:
            dicta[key] = dictb[key]
        #``26
    #``24
#``23

# MakeCnfException is thrown when the config file was just created, for clients to
# catch it, display it, and exit quietly.  29``/MakeCnfException:
class MakeCnfException(Exception):
    def __init__(self, message:str):
        super().__init__(message)
#``29
#``1
