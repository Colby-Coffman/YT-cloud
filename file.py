import os
import re

def get_interactively(directory=None, message = "Select file", filter=None):
    if directory == None: directory = os.getcwd()
    try:
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtWidgets import QFileDialog
    except ImportError:
        raise ImportError("PyQt5 is a required dependency for file picking")
    app = QApplication([])
    file, filter = QFileDialog.getOpenFileName(directory=directory, caption=message,
                                       filter=filter)
    if file == "":
        raise FileNotFoundError("No file was selected")
    app.exit()
    return file

class InvalidType(Exception): pass

def validate(path):
    cwd = os.getcwd()
    exists = os.path.exists(path)
    if not exists:
        exists = os.path.exists(os.path.join(cwd, path))
        if not exists:
            raise FileNotFoundError("The passed file cannot be found")
        else:
            path = os.path.join(cwd, path)
    if not os.path.isfile(path) or os.path.islink(path):
                raise InvalidType("The file passed must be a file, not a link or directory")
    
def find_secret(path=__file__):
    dir = os.path.dirname(path)
    secret = None
    for path in os.listdir(dir):
        match = re.search("^client_secret.*\.json$", path)
        if match:
            secret = path
    if secret: return secret
    else: raise FileNotFoundError(f"No client_secrets file found in {path}")

def get_title(path):
    head, tail = os.path.split(path)
    return tail.split(".")[0]