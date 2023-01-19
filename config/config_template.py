#!/usr/bin/env python

# ----------------------------------------------------------------
# IMPORTANT NOTES TO DEVELOPERS
# 1 - MAKE A COU OF THIS FILE AND REMOVE THE "_template" PART
# 2 - THE .GITIGNORE INCLUDES A PATTERN TO NOT COMMIT THIS FILE, 
# BUT MAKE SURE IT DOES NOT GET INCLUDED IN ANY OF YOUR COMMITS
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# REPLACE THE FOLLOWING VARIABLES WITH YOUR OWN
# ----------------------------------------------------------------
node_name    = 'MYFLNODE'
path_to_csv  = '/absolute/path/to/csv/or/excel/file.csv'
path_to_code = '/absolute/path/where/you/want/to/store/federated_learning_code'
data_path    = '/absolute/path/to/data/folder/containing/images'

# ----------------------------------------------------------------
# REPLACE THE FOLLOWING VARIABLES WITH THE PROJECT'S VALUES
# ----------------------------------------------------------------
central_server_ip   = 'ip.for.central.node'
central_server_port = 1234
central_flower      = 'ip.for.central.flower.server'
central_flower_port = 1234
docker_image_name   = 'registry.gitlab.bsc.es/bfp/fl_breast_mg_classification'
github_repo_name    = 'https://github.com/UBFL/FLClient.git'