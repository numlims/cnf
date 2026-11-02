# __init__.py was generated from init.ct. 
# if you edit __init__.py, run `ct -tc __init__.py` afterwards to update init.ct.
# when editing this file leave the `` tags.
#``ct version 0.1.1
#``ct files init.ct __init__.py

# # cnf
# 
# cnf creates and loads configuration files.  1``//__init__.py:
# imports for init.  8``/import:
import os
# imports for handleflag.  15``/import
import json
# imports for cnfpath.  23``/import
from pathlib import Path
# imports for _load.  35``/import
import yaml
import json
import configparser
#``8
# the root constants.  7``/const:
user = "user"  # in the user's home directory
system = "system"  # system wide
#``7
class cnf:
    # init initializes a cnf instance makeload reads the conf file(s) at `path` rooted in cnf.user,
    # cnf.system or both and parses them from a given format, subsequent
    # values overwriting values before.
    # 
    # if no config file is there it creates one at the first writable root from `make`.
    # 
    # `company` is needed for the windows config paths.
    # 
    # if no config file was there and it was created, a `MakeCnfException` is
    # thrown.   2``/init:
    def __init__(self, path:str=None, roots:str=None, company:str=None, fmt:str=None, make:str=None):
        # resolve the complete paths.
        # 
        # if the home can't be resolved, _cnfpath returns None, check for that.  3``_:
        self.paths = []  # TODO make this a method or so?
        for root in roots:
            p = _cnfpath(root, path, company=company)
            if p is not None:
                self.paths.append(p)
        # try to load files at the resoled paths.  keep track of whether at any
        # of the paths there is an actual file.  4``
        anyexists = False
        mergedcontent = {}
        for p in self.paths:
            (exists, content) = _load(p, fmt)
            if exists:
                anyexists = True
            _overwrite(mergedcontent, content)
        # if there isn't a file at any of the paths, create one from
        # make-template at the first writeable path.  5``
        if not anyexists:
            _makewriteable(make, self.paths)
        # return whatever content was loaded (and merged) from the one or more
        # roots.  6``
        self.conf = mergedcontent
        #``3
    #``2
    # addflags adds --conf-path and --conf flags to an argument parser.  9``/addflags:
    def addflags(self, parser):
        # add the flags.  10``_:
        parser.add_argument("--conf-path", action="store_true", help="show config path(s)", required=False)
        parser.add_argument("--conf", action="store_true", help="show loaded config", required=False)    
        #``10
    #``9
    # handleflag looks for the --conf-path and --conf flags in parsed
    # argparse arguments. return whether one of the flags was handled.  11``/handleflag:
    def handleflag(self, args):
        # print the config path(s) for the --conf-path flag.  12``_:
        if args.conf_path:
            for p in self.paths:
                print(p)
            return True
        # print the loaded config for the --conf flag.  13``
        if args.conf:
            print(json.dumps(self.conf, indent=4))
            return True
        # if no flag was handled return false.  14``
        return False
        #``12
    #``11
    
# _cnfpath appends path to root, which can be cnf.user or cnf.system.  if the user's home can't be resolved, None is returned.
# company is needed for the windows config paths.  16``/_cnfpath:
def _cnfpath(root, path, company=None):
    # in windows both local and system wide config paths need a company
    # name, so give an error if no company specified.  17``_:
    if company is None:
        raise Exception(f"cnf: company needs to be specified for windows config paths.")
    # get the root constant.  18``
    rootpath = ""
    if root == None:
        rootpath = ""
    elif root == user:
        # the user location of conf files is ~/.config/ for posix and USERPROFILE/AppData/Local/<company>/ for windows.
        # 
        # for windows, see https://learn.microsoft.com/en-us/archive/blogs/patricka/where-should-i-store-my-data-and-configuration-files-if-i-target-multiple-os-versions
        # 
        # return None if python can't determine the home directory.  19``./user:
        if os.name == "posix":
            try:
                rootpath = os.path.join(Path.home(), ".config/")
            except Exception as e:
                return None
        elif os.name == "nt":
            try:
                rootpath = os.path.join(Path.home(), f"AppData/Local/{company}")
            except Exception as e:
                return None
        else:
            raise Exception(f"cnf: no user config location for os {os.name}.")
        #``19
    elif root == system:
        # the system-wide location of conf files is /etc/ for posix and C:\ProgramData\<company>\<app> for windows.  20``../system:
        if os.name == "posix":
            rootpath = os.path.join("/etc/")
        elif os.name == "nt":
            rootpath = os.path.join(f"/ProgramData/{company}/")
        else:
            raise Exception(f"cnf: no system-wide config location for os {os.name}.")
        #``20
    # else say the root is not known.  21``/_cnfpath/_
    else:
        raise Exception(f"cnf: root {root} not known.")
    # append the path given by the user.  22``
    return os.path.join(rootpath, path)
    #``17
#``16
# _makewriteable makes a stub conf file at the first writeable path.  24``/_makewriteable:
def _makewriteable(make:str, paths:list):
    # go over the paths, check if they are writeable.  25``_:
    anywriteable = False            
    for p in paths:
        if os.access(os.path.dirname(p), os.W_OK):
            # make the file.  26``./write:
            anywriteable = True
            _make(p, make) 
            # send a MakeCnfException that can be caught by the calling program to exit gracefully.
            # 
            # give the other path(s) where the config file also could be placed, if that's the case.  27``
            msg = f"stub config file created at {p}, please edit."
            plist = ""
            for path in paths:
                if path != p:
                    plist += f"\n{path}"
            if plist != "":
                msg += f"\nyou can leave the config file there or move it to:{plist}"
            raise MakeCnfException(msg)
            return None
            #``26
    # raise an exception if none of the paths were writeable.  28``/_makewriteable/_
    if not anywriteable:
        raise Exception(f"cnf: none of the config paths {paths} was writable, please try to put a config file there manually using this template: \n{make}")  # TODO should this be a MakeCnfException?  or another custom exception?
        return None
    #``25
#``24
# _make creates a stub config file at path p.  29``/_make:
def _make(p:str, content:str):
    if os.path.exists(p):
        raise Exception(f"cnf: file exists at {p}, not overwriting it.")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as file:
        file.write(content)
#``29
# _load loads the config file at path, parsing it as fmt.  30``/_load:
def _load(p:str, fmt:str):
    # from the returned content can't be inferred whether the file exists (an empty yaml file parses as None, not as an empty dict), so return whether the file exists.  31``_:
    exists = os.path.exists(p)
    # configparser doesn't need an opened file, it reads a path.  32``
    if fmt == "ini":
        config = configparser.ConfigParser()
        config.read(p)
        # convert to dict for easier json output.  33.``
        d = {}
        for k in config.keys():
            items = config.items(k)
            d[k] = dict(items)
        return (exists, d)
        #``33
    # read the other formats from opened file.  34``/_load/_
    else:
        with open(p, "r") as file:
            if fmt == None:
               return (exists, file.read())
            elif fmt == "yaml":
               return (exists, yaml.safe_load(file))
            elif fmt == "json":
               return (exists, json.load(file))
            else:
               print(f"{fmt} not known.")
               return (exists, None)
    #``31
#``30
# _overwrite overwrites the values in dicta with what's in dictb.  36``/_overwrite:
def _overwrite(dicta=None, dictb=None):
    # do nothing if dictb is None.  37``_:
    if dictb is None:
        return
    # go over the keys in dict b.  38``
    for key in dictb:
        # key is not in dicta: just put it in.  39.``
        if not key in dicta:
            dicta[key] = dictb[key]
        # dictb at key is a map: recurse.  40``
        elif isinstance(dictb[key], dict):
            _overwrite(dicta[key], dictb[key])
        # dictb at key is not a map: overwrite.  41``
        else:
            dicta[key] = dictb[key]
        #``39
    #``37
#``36

# MakeCnfException is thrown when the config file was just created, for clients to
# catch it, display it, and exit quietly.  42``/MakeCnfException:
class MakeCnfException(Exception):
    def __init__(self, message:str):
        super().__init__(message)
#``42
#``1
