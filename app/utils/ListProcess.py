import psutil

def SortPName (data):
    return data[0]

def ListProcess():
    plist = []
    for proc in psutil.process_iter():
        try:
            # Get process name & pid from process object.
            processName = proc.name()
            processID = proc.pid
            percent = proc.cpu_percent()

            plist.append( (processName, proc.pid, percent))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    plist.sort(key=SortPName)

    return plist