import subprocess
import os
import time
import pika
from pathlib import Path

#function to check the installations and resources of the center
def start_client(n):
    print("Starting docker")
    try:
        path_to_csv = os.environ['PATH_TO_CSV']
        path_to_code = os.environ['PATH_TO_CODE']
        data_path = os.environ['DATA_PATH']
        quick_run = True  # os.environ['QUICK_RUN']
        docker_image_name = os.environ['DOCKER_IMAGE_NAME']
        central_ip = os.environ['FLOWER_CENTRAL_SERVER_IP']
        central_port = os.environ['FLOWER_CENTRAL_SERVER_PORT']
        command = f"docker run -d --shm-size=12GB \
                    -v {path_to_code}:/FL/Code \
                    -v {data_path}:{data_path} \
                    -v {path_to_csv}:{path_to_csv} \
                    -e QUICK_RUN={quick_run} \
                    -e PATH_TO_CSV={path_to_csv}\
                    -e FLOWER_CENTRAL_SERVER_IP={central_ip} \
                    -e FLOWER_CENTRAL_SERVER_PORT={central_port} \
                    {docker_image_name} \
                    python3 /FL/Code/FLClient/main.py"
        print('EXECUTING COMMAND:', command)
        check = subprocess.run(command, shell=True, capture_output=True)
        response = check.stdout.decode()
        return response
    except Exception as e:
        print(f"Error starting Docker.\nTraceback: {e}")
