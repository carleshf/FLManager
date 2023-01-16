import subprocess
import os
import time
import pika

#function to check the installations and resources of the center
def stop_client(n):
    print ("stoping")
    try:
        command = f"docker stop {n}"
        print('EXECUTING COMMAND', command)
        check = subprocess.run(command, shell=True, capture_output=True)
        response = check.stdout.decode()
        return response
    except Exception as e:
        print(f"Error stopping docker image with id: {n}\nTraceback: {e}")
