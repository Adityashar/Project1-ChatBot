import os, subprocess

#activate env
#move to dir

def main():
    pid = subprocess.run('pgrep -f bin/rasa', shell=True, check=True, stdout=subprocess.PIPE).stdout.decode()

    pids = pid.split('\n')[:-2]
    kill_pid = "kill -9 "
    for id in pids:
        kill_pid += id + " "

    print(pids)

    if len(pids) > 0:
        subprocess.run(kill_pid, shell=True)

    print("==========================================\n\nProcesses have been killed!!\n\n==========================================")

# train the model
    subprocess.run('rasa train', shell= True)

    print("==========================================\n\nModel has been trained!!\n\n==========================================")

# run the shell
    subprocess.run('rasa run -m models --enable-api --cors "*" --debug', shell=True)



if __name__ == '__main__':
    main()
