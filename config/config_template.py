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
node_name     = 'MYFLNODE'
path_to_csv   = '/absolute/path/to/csv/or/excel/file.csv'
path_to_code  = '/absolute/path/where/you/want/to/store/federated_learning_code'
data_path     = '/absolute/path/to/data/folder/containing/images'
node_user     = 'a-cool-node-of-the-fl-network'
node_password = 'a-strong-password'
cert_phrase   = 'a-stronger-password'

# ----------------------------------------------------------------
# REPLACE THE FOLLOWING VARIABLES WITH YOUR OWN
# ----------------------------------------------------------------
ssl_active              = True
ssl_central_server_port = 1234
ssl_cafile_path         = '/path/o/cer/ca_certificate.pem'
ssl_client_cert_path    = '/path/o/cer/client_certificate.pem'
ssl_client_keys_path    = '/path/o/cer/client_key.pem'

# ----------------------------------------------------------------
# REPLACE THE FOLLOWING VARIABLES WITH THE PROJECT'S VALUES
# ----------------------------------------------------------------
central_server_ip   = 'ip.for.central.node'
central_server_port = 1234
central_flower      = 'ip.for.central.flower.server'
central_flower_port = 1234
docker_image_name   = 'registry.gitlab.bsc.es/bfp/fl_breast_mg_classification'
github_repo_name    = 'https://github.com/UBFL/FLClient.git'
