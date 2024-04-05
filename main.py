import socket
import time
import os

os.system("clear")
def get_file_size(file_path):
    if not os.path.exists(file_path):
        return -1
    size = os.path.getsize(file_path) / (1024*1024)
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        lines[0] = f"Size: {size}MB\n"
        file.seek(0)
        file.writelines(lines)

def is_connected():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

def log_connection_status(connected, counters, logfile):
    current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    status = "CONNECTED" if connected else "DISCONNECTED"
    counters["c" if connected else "d"] += 1
    log_message = f"{status} {current_time}\n"

    try:
        with open(logfile, "a") as f:
            f.write(log_message)
        color = "\033[32m" if connected else "\033[91m"
        print(f"{color}{log_message}\033[0m")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def main():
    logfile = r"???"
    print("you need to change the logfile variable on line 38 to the filepath to your log file."),exit() if logfile == r"???" else pass
    counters = {"c":0,"d":0}
    with open(logfile, "r") as f:
        log_content = f.read()
        print(log_content)
        counters["c"] = int(log_content.split("[")[1].split("]")[0])
        counters["d"] = int(log_content.split("[")[2].split("]")[0])

        

    
    while True:
        with open(logfile, 'r+') as file:
            lines = file.readlines()
            lines[1] = f"Connected:[{counters['c']}] disconnected:[{counters['d']}]\n"
            file.seek(0)
            file.writelines(lines)
        
        get_file_size(logfile)
        connected = is_connected()
        log_connection_status(connected, counters, logfile) 
        time.sleep(1)

if __name__ == "__main__":
    main()
