from os import path, listdir

def check_directories(dir):
    if not path.exists(dir) or listdir(dir) == []:
        return False
    else:
        return True
        