import time

def getCurrentTimeStamp():
    return int(str(time.time()).split(".")[0])