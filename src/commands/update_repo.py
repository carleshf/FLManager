import os 
import subprocess

def update_repo(n):
    repo = os.environ['GITHUB_REPO_NAME']
    workdir = os.environ['PATH_TO_CODE']
    if (n=="clone"):
        try:
            command = f"git clone {repo} {workdir}/FLClient"
            print('EXECUTING COMMAND', command)
            check = subprocess.run(command, shell=True, capture_output=True)
            response = check.stdout.decode()
            print (response)
            return response
        except Exception as e:
            print(f"Cannot clone the GitHub repo.\nTraceback: {e}")
    elif (n=="pull"):
        try:
            command = f"git -C {workdir}/FLClient pull {repo}"
            print('EXECUTING COMMAND', command)
            check = subprocess.run(command, shell=True, capture_output=True)
            response = check.stdout.decode()
            print (response)
            return response
        except Exception as e:
            print(f"Cannot pull the GitHub repo.\nTraceback: {e}")
    else:
        print(f"Invalid command: {n}")