 # FL_rabbit
Build:
`docker-compose build`

Run RabbitMQ in a Docker container:
`docker-compose up`


For the centers-->
`bash setup.sh`: it should install whatever and clone the needed repos (FLManager and the model) + run recieve.py


The user that is logged in that computer should be part of the docker group to be able to run the docker image without using sudo. If not, this can be enabled doing: 
`sudo groupadd docker`
`sudo usermod -aG docker $USER`
`newgrp docker`

# rpc commands
[x] self_check()

    [x]installation
    [x]rabbit
    [x]gpus

[x] update_repo()

    [x]repo

[x] update_image()

    [-]image (Takes too long, timeout 60)

[x] start_client()

    [-]client
    
[x] stop_client()

    [-]container id


# FLManager
