"""
Dynamic Training Module
"""

import subprocess

#activate env
#move to dir

def main():
    """main function"""
    pid = subprocess.run('pgrep -f bin/rasa', shell=True, check=True, stdout=subprocess.PIPE).stdout.decode()

    pids = pid.split('\n')[:-2]
    kill_pid = "kill -9 "
    for i_d in pids:
        kill_pid += i_d + " "
    print(pids)

    if len(pids) > 0:
        subprocess.run(kill_pid, shell=True, check=True)

    print("==========================================\n")
    print("Processes have been killed!!\n")
    print("==========================================")

# train the model
    subprocess.run('rasa train', shell=True, check=True)

    print("==========================================\n")
    print("Model has been trained!!\n")
    print("==========================================")

# run the shell
    subprocess.run('rasa run -m models --enable-api --cors "*" --debug', shell=True, check=True)



if __name__ == '__main__':
    main()
