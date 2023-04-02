from datetime import datetime

def time_now() :
    now = datetime.now()
    time_now = now.strftime("#[%H/%M/%S]")
    return time_now