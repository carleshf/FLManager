#!/usr/bin/env python

import os 
import sys
import ssl
import pika
import time
import subprocess
    
from src.commands import *
import src.commands as afun
from inspect import getmembers, isfunction

def valid_command(command, against):
    command = str(command).split('(')
    if len(command) != 2:
        return 1, 'not valid'
    if command[0] not in against:
        return 2, 'not valid'
    return 0, 'valid'


# LOAD FUNCTION OPEN TO RABBITMQ
av_func = [ x[0] for x in getmembers(afun, isfunction) ]
if len( av_func ) < 1:
    print('[x] Once we loaded the python module with function exposed to RabbitMQ, no one was available..')
    sys.exit(1)

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
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host = config.central_server_ip,
                port = config.central_server_port,
                heartbeat = 600,
                blocked_connection_timeout = 300
            )
        )
except Exception as e:
    print(f'[x] RabbitMQ connection error. RabbitMQ server not found.')
    print(e)
    sys.exit(1)

queue_name = config.node_name
channel = connection.channel()
channel.queue_declare(queue = queue_name)

def on_request(ch, method, props, body):
    """Commands list:
    self_check installation
    self_check gpus
    update_image pull
    update_repo clone
    update_repo pull
    start_client
    stop_client container_id
    """
    n = body.decode('utf-8')
    v = valid_command(n, av_func)
    print(f'[.] Received command "{n}" that is {v[1]}') 
    if v[0] == 1:
        print(f'[x] Receved command does not follow an accepted format.')
        response = "Invalid format"
    elif v[0] == 2:
        print('[x] Receved command is invalid because it is not exposed to RabbitMQ.')
        response = "Not exposed function"
    else:
        try:
            response = eval(n)
            if response == None:
                response = f'Command not found {n}'
            print('RESPONSE:', response)
        except Exception as e:
            response = f'Error raised when evaluating the command'
            print(e)
            print(f'[x] Got error: {e}')

    ch.basic_publish(exchange = '', routing_key = props.reply_to, properties = pika.BasicProperties(correlation_id = props.correlation_id), body = response)
    ch.basic_ack(delivery_tag = method.delivery_tag)

    print(f"[.] Done processing {n}")
    print(f"[.] Awaiting for requests")
    
channel.basic_qos(prefetch_count = 1)
channel.basic_consume(queue = queue_name, on_message_callback = on_request)
print("[.] Awaiting for requests")
channel.start_consuming()
