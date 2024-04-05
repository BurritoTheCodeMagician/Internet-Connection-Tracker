import socket
import time
import os

def get_file_size(file_path):
    if not os.path.exists(file_path):
        return -1
    size = os.path.getsize(file_path) / (1024*1024)
    with open(file_path, 'r+') as file:
        lines = file.readlines()
        if len(lines) == 0:
            lines.append("Size: 0MB\nConnected:[0] disconnected:[0]\n")
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
    # Set default log file path
    default_logfile = "connection_log.txt"
    
    # Check if log file exists, if not, create it
    if not os.path.exists(default_logfile):
        with open(default_logfile, "w") as f:
            f.write("Size: 0MB\nConnected:[0] disconnected:[0]\n")

    counters = {"c": 0, "d": 0}

    while True:
        # Update log file with connection status and size
        get_file_size(default_logfile)
        connected = is_connected()
        log_connection_status(connected, counters, default_logfile) 
        time.sleep(1)

if __name__ == "__main__":
    main()
