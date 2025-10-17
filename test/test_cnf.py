import cnf
import os
import shutil
def test_makeload():
    """
    test_makeload checks whether makeload makes a file.
    """
    config = _tryconf("yaml", "a: b")
    assert config["a"] == "b"
    content = """
[a]
b = c
"""
    config = _tryconf("ini", content)
    assert config["a"]["b"] == "c"
def _tryconf(fmt, content):
    """
    """
    path = "test/try/conf"
    if os.path.exists("test/try"):
        shutil.rmtree("test/try")
    cnf.makeload(path, fmt=fmt, make=content)
    assert os.path.exists(path)
    config = cnf.makeload(path, fmt=fmt, make=content)
    shutil.rmtree("test/try")
    return config
