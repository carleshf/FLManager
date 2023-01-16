#!/bin/bash

# ----------------------------------------------------------------
# REPLACE THE FOLLOWING VARIABLES WITH YOUR OWN
# ----------------------------------------------------------------
# NOTE TO DEVELOPERS: DO NOT COMMIT THIS FILE WITH YOUR OWN VALUES
# ----------------------------------------------------------------
export PATH_TO_CSV=/absolute/path/to/csv/or/excel/file.csv
export PATH_TO_CODE=/absolute/path/where/you/want/to/store/federated_learning_code
export DATA_PATH=/absolute/path/to/data/folder/containing/images
#export HOSPITAL_NAME=ub
export HOSPITAL_NAME=aristotle-university-thesaloniki
#export HOSPITAL_NAME=germans-trias-i-pujol
#export HOSPITAL_NAME=gumed
#export HOSPITAL_NAME=hospital-italiano-de-buenos-aires
#export HOSPITAL_NAME=la-fe-university-and-polytechnic-hospital
#export HOSPITAL_NAME=upenn
#export HOSPITAL_NAME=parc-tauli

# ----------------------------------------------------------------
# DO NOT CHANGE THE FOLLOWING VARIABLES
# ----------------------------------------------------------------
export CENTRAL_SERVER_IP=84.88.189.135
export CENTRAL_SERVER_PORT=5672
export FLOWER_CENTRAL_SERVER_IP=84.88.186.195
export FLOWER_CENTRAL_SERVER_PORT=8080
export DOCKER_IMAGE_NAME=registry.gitlab.bsc.es/bfp/fl_breast_mg_classification
export GITHUB_REPO_NAME=https://github.com/UBFL/FLClient.git

pip install -r requirements.txt

python3 start.py
