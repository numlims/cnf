import cnf
import os
import shutil
def test_makeload():
    """
    test_makeload checks whether makeload makes a file.
    """
    path = "test/try/conf"
    if os.path.exists("test/try"):
        shutil.rmtree("test/try")
    content = "a: b"
    cnf.makeload(path, fmt="yaml", make=content)
    assert os.path.exists(path)
    config = cnf.makeload(path, fmt="yaml", make=content)
    assert config["a"] == "b"
    shutil.rmtree("test/try")
