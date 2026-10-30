# test_cnf.py was generated from test.ct. 
# if you edit test_cnf.py, run `ct -tc test_cnf.py` afterwards to update test.ct.
# when editing this file leave the `` tags.
#``ct version 0.1.1
#``ct files test.ct test_cnf.py

# test contains tests for cnf.  1``//test_cnf.py:
# import.  11``/import:
import cnf
import os
import shutil
#``11
# test_makeload checks whether makeload makes a file.  2``/test_makeload:
def test_makeload():
    # try yaml.  3.``
    try:
        config = _tryconf("yaml", "a: b")
        assert config["a"] == "b"
    except cnf.MakeCnfException:
        pass
    # try ini.  4``
    content = """
[a]
b = c
"""
    try:
        config = _tryconf("ini", content)
        assert config["a"]["b"] == "c"
    except cnf.MakeCnfException:
        pass
    #``3
#``2
# _createconfig creates a conf file, returns its contents and cleans up.  5``/_tryconf:
def _tryconf(fmt, content):
    # remove the output folder if already there.  6.``
    path = "test/try/conf"
    if os.path.exists("test/try"):
        shutil.rmtree("test/try")
    # `shutil.rmtree()` removes a directory and all its contents. `os.remove()` only
    # works for files, `pathlib.Path.rmdir()` only works for empty dirs.
    # 
    # create the conf file and check that if exists.  7``
    cnf.makeload(path, fmt=fmt, make=content)
    assert os.path.exists(path)
    # load the config.  8``
    config = cnf.makeload(path, fmt=fmt, make=content)
    # remove the created files again.  9``
    shutil.rmtree("test/try")
    # return for checking.  10``
    return config
    #``6
#``5
#``1
