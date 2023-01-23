#!/usr/bin/env python

import sys
import ssl
import pika
import argparse
import uuid
import multiprocessing

from pathlib import Path
from amqpstorm import management

# ACCEPTED NODE LIST TO SEND WORKS
node_list = [
    'MYLOCALHOST1',
    'MYLOCALHOST2'
#"UB",
#"BUCH",
#"GEM",
#"ICRC",
#"KUH",
#"UCL",
#"UMCU",
#"AUMC",
#"VHIR",
]

# LOAD CONFIGURATION
try:
    import config.config as config
except:
    print(f'[x] Configuration file not found or has an invalid format.')
    sys.exit(1)

















# # CREATE RABBITMQ CONNECTION AND QUEUE
# #mq_connection = "amqp://guest:guest@84.88.189.135:5672/%2F"
# mq_connection = "amqp://guest:guest@localhost:5672/%2F"
# parameters = pika.URLParameters(mq_connection)

# #https://www.rabbitmq.com/ssl.html
#  # if mq_connection.startswith('amqps'):
#  #     context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
#  #     context.check_hostname = False

#  #     cacertfile = Path('/home/user/LocalEGA/tests/_common/mq/CA.cert.pem')
#  #     certfile   = Path('/home/user/LocalEGA/tests/_common/mq/testsuite.cert.pem')
#  #     keyfile    = Path('/home/user/LocalEGA/tests/_common/mq/testsuite.sec.pem')

#  #     context.verify_mode = ssl.CERT_NONE

#  #     # Require server verification
#  #     if cacertfile.exists():
#  #         context.verify_mode = ssl.CERT_REQUIRED
#  #         context.load_verify_locations(cafile=str(cacertfile))

#  #     # If client verification is required
#  #     if certfile.exists():
#  #         assert( keyfile.exists() )
#  #         context.load_cert_chain(str(certfile), keyfile=str(keyfile))

#  #     # Finally, the pika ssl options
#  #     parameters.ssl_options = pika.SSLOptions(context=context, server_hostname=None)




# LOAD CONFIGURATION
try:
    import config.config as config
except:
    print('[x] Configuration file not found or has an invalid format.')
    sys.exit(1)


# LOADING CERTIFICATES FOR SSL INTEGRATION
try:
    if config.ssl_active:
        context = ssl.create_default_context(cafile = config.ssl_cafile_path)
        context.load_cert_chain(config.ssl_client_cert_path, config.ssl_client_keys_path, password = config.cert_phrase)
        ssl_options = pika.SSLOptions(context, config.central_server_ip)
        credentials = pika.PlainCredentials(config.node_user, config.node_password)
except Exception as e:
    print('[x] Error loading client certificates for RabbitMQ secure conection.')
    sys.exit(1)

# CREATE RABBITMQ CONNECTION AND QUEUE
try:
    if config.ssl_active:
        params = pika.ConnectionParameters(
            port = config.ssl_central_server_port,
            ssl_options = ssl_options,
            credentials = credentials
        )
        connection = pika.BlockingConnection(params)
    else:
        params = pika.ConnectionParameters(
            host = config.central_server_ip,
            port = config.central_server_port,
            heartbeat = 600,
            blocked_connection_timeout = 300
        )
except Exception as e:
    print(f'[x] RabbitMQ connection error. RabbitMQ server not found.')
    print(e)
    sys.exit(1)


class RpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue = self.callback_queue,
            on_message_callback = self.on_response,
            auto_ack = True
        )

        self.response = None
        self.corr_id = str(uuid.uuid4())

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, n, node):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange = '',
            routing_key = node,
            properties = pika.BasicProperties(
                reply_to = self.callback_queue,
                correlation_id = self.corr_id,
            ),
            body = str(n)
        )
        #connection.process_data_events() #this is blocking
        self.connection.process_data_events(time_limit = None)
        return self.response

def start_call(idx, rst, command, node):
    try:
        rpc = RpcClient()
        print(f'[.] Requesting {command} to {node}')
        response = rpc.call(command, node)
        print(f'[.] Response from {node}: {response}')
        rst[idx] = 0
    except pika.exceptions.AMQPConnectionError as e:
        print(f'[x] RabbitMQ connection error with node {node}. RabbitMQ server not found.')
        rst[idx] = 1
    except Exception as e:
        print(e)
        print(f'[x] Error from node {node}: {e}')
        rst[idx] = 1


if __name__ == '__main__':
    
    #get arguments from command line using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--function", help="function to call, default self_check", 
                        choices=['start_client', 'self_check', 'update_repo', 'update_image', 'stop_client', 'test_time'],
                        type=str, required=True, nargs='?')
    parser.add_argument("--argument", help="argument to pass to function: self_check(installation, gpus, paths, data), start_client(client), update_repo(clone, pull), update_image(pull), stop_client(docker_id)", required=True, nargs='?')
    args = parser.parse_args()
    function = args.function
    assert function in ['start_client', 'self_check', 'update_repo', 'update_image', 'stop_client'], f"fuenction {function} not in list"
    argument = args.argument
    if function == 'self_check':
        assert argument in ['installation', 'gpus', 'paths', 'data'], f"argument {argument} not in list, use installation, gpus, paths, data"
    if function == 'start_client':
        assert argument in ['client'], f"argument {argument} not in list, use client"
    if function == 'update_repo':
        assert argument in ['clone', 'pull'], f"argument {argument} not in list, use clone or pull"
    if function == 'update_image':
        assert argument in ['pull'], f"argument {argument} not in list, use pull"
    if function == 'stop_client':
        assert len(argument) > 0, f"argument must be the docker id that is returned by start_client(client)"
    if function == 'test_time':
        argument = ''

    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    jobs = []
    command = f"{function}('{argument}')"
    for idx, node in enumerate(node_list):
       #start process start_call
        p = multiprocessing.Process(target=start_call, args=(idx, return_dict, command, node,))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    if(sum(return_dict.values()) > 0):
        sys.exit(1)
