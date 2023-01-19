#!/bin/bash

# ----------------------------------------------------------------
# REPLACE THE FOLLOWING VARIABLES WITH YOUR OWN
# ----------------------------------------------------------------
# NOTE TO DEVELOPERS: DO NOT COMMIT THIS FILE WITH YOUR OWN VALUES
# ----------------------------------------------------------------
export PATH_TO_CSV=/absolute/path/to/csv/or/excel/file.csv
export PATH_TO_CODE=/absolute/path/where/you/want/to/store/federated_learning_code
export DATA_PATH=/absolute/path/to/data/folder/containing/images
#export HOSPITAL_NAME=UB
#export HOSPITAL_NAME=BUCH
#export HOSPITAL_NAME=GEM
#export HOSPITAL_NAME=ICRC
#export HOSPITAL_NAME=KUH
#export HOSPITAL_NAME=UCL
#export HOSPITAL_NAME=UMCU
#export HOSPITAL_NAME=AUMC
#export HOSPITAL_NAME=VHIR

# ----------------------------------------------------------------
# DO NOT CHANGE THE FOLLOWING VARIABLES
# ----------------------------------------------------------------
export CENTRAL_SERVER_IP=84.88.189.140
export CENTRAL_SERVER_PORT=5672
export FLOWER_CENTRAL_SERVER_IP=84.88.189.140
export FLOWER_CENTRAL_SERVER_PORT=8080
export DOCKER_IMAGE_NAME=registry.gitlab.bsc.es/bfp/fl_breast_mg_classification
export GITHUB_REPO_NAME=https://github.com/UBFL/FLClient.git

pip install -r requirements.txt

python3 start.py
