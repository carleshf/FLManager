import subprocess
import threading
import time
import os

def update_image(n):
    docker_image_name = os.environ['DOCKER_IMAGE_NAME']
    if (n=="pull"): 
        try:
            command = f"docker pull {docker_image_name}"
            print('EXECUTING COMMAND', command)
            check = subprocess.run(command, shell=True, capture_output=True)
            response = check.stdout.decode()
            print(response)
            return response
        except Exception as e:
            print(f"Error pulling the docker image {docker_image_name}.\nTraceback: {e}")
    else:
        print(f"Invalid command: {n}")

