import subprocess
import time

def start_stop(exe_name):
    proc = subprocess.Popen(exe_name, shell=True)
    time.sleep(5)
    proc.terminate()
    time.sleep(5)

def kill_by_pid(pid):
    proc = subprocess.run(["taskkill","/pid",pid], capture_output = True)
    return proc.check_returncode

def get_pid_from_tasklist(app_name):
    proc = subprocess.run("tasklist", capture_output = True)
    for line in proc.stdout.decode().split("\n"):
        if line.find(app_name) != -1:
            return line.split()[1]
            

if __name__ == "__main__":
    target_executable = "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    target_process_name = "firefox.exe"

    start_stop(target_executable)

    subprocess.Popen("C:\\Program Files\\Mozilla Firefox\\firefox.exe")
    time.sleep(10)
    kill_by_pid(get_pid_from_tasklist(target_process_name))