import subprocess
import os
import pika
from pathlib import Path
import pandas as pd

from src.utils.validator import validate_csv

#function to check the installations and resources of the center
def self_check(n):
    if (n=="installation"):
        try:
            command = "docker --version; curl ipinfo.io"
            print('EXECUTING COMMAND', command)
            check = subprocess.run(command, shell=True, capture_output=True)
            response = check.stdout.decode()
            print (response)
            return response
        except Exception as e:
            print(f"Error calling Docker. If the user running the bash script is not part of the docker group, please add it with the following commands: 1) `sudo groupadd docker`, 2)`sudo usermod -aG docker $USER`, 3)`newgrp docker`.\nTraceback: {e}")
    elif (n=="gpus"):
        try:
            check = subprocess.check_output('nvidia-smi')
            #response = 'Nvidia GPU detected'
            response = check
            print('Nvidia GPU detected')
            return response
        except Exception as e: 
            print(f'No Nvidia GPU in system.\nTraceback: {e}')
            response= 'No Nvidia GPU in system'
            return response
    elif (n=="paths"):
        path_to_csv = Path(os.environ['PATH_TO_CSV'])
        path_to_code = Path(os.environ['PATH_TO_CODE'])
        data_path = Path(os.environ['DATA_PATH'])
        response = ""
        if not path_to_csv.exists():
            print(f"Path to csv file does not exist: {path_to_csv}")
            response += f"Path to csv file does not exist: {path_to_csv}\n"
        if not path_to_code.exists():
            print(f"Path to code does not exist: {path_to_code}")
            response += f"Path to code does not exist: {path_to_code}\n"
        if not data_path.exists():
            print(f"Path to data does not exist: {data_path}")
            response += f"Path to data does not exist: {data_path}\n"
        if response == "":
            print("Data paths are valid")
            response = "Data paths are valid"
        return response
    elif (n=="data"):
        print("Checking csv format")
        print("A")
        template_csv = Path.absolute(Path(__file__).parent.parent / "templates" / "federated_data_info_csv_template.csv")
        dataset_csv = Path(os.environ['PATH_TO_CSV'])
        primary_keys = None  # ["client_id"]
        non_nan_columns = ["client_id", "status", "image_filepath"]
        imagepath_column_name = "image_filepath"
        # read template csv file
        template = pd.read_csv(template_csv)

        # read dataset csv file
        dataset = pd.read_csv(dataset_csv)

        # validation
        is_valid = validate_csv(template=template, dataset=dataset, primary_keys=primary_keys,
                                non_nan_columns=non_nan_columns, imagepath_column_name=imagepath_column_name)
        if not is_valid[0]:
            response = f"The provided dataset {dataset_csv} is not valid. Reason: {is_valid[1]}"
        else:
            response = f"{is_valid[1]}"
        return response
    else:
        print(f"Invalid command: {n}")
