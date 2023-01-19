#!/usr/bin/env python

import os 
import sys
import pika
import time
import subprocess

from src.commands import *

# LOAD CONFIGURATION
try:
    import config.config as config
except:
    print(f'[x] Configuration file not found or has an invalid format.')
    sys.exit(1)

# CREATE RABITMQ CONNECTION AND QUEUE
try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host = config.central_server_ip, port = config.central_server_port, heartbeat = 600, blocked_connection_timeout = 300)
        #pika.ConnectionParameters(host = os.environ["CENTRAL_SERVER_IP"], port = os.environ["CENTRAL_SERVER_PORT"], heartbeat = 600, blocked_connection_timeout = 300)
    )
except:
    print(f'[x] RabbitMQ connection error. RabbitMQ server not found.')
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
    print(f'[.] Received {n}') 
    try:
        response = eval(n)
        if response == None:
            response = f'Command not found {n}'
        print('RESPONSE:', response)
    except Exception as e:
        response = f'Error raised when evaluating the command'
        print(f'[x] Got error: {e}')

    ch.basic_publish(exchange = '', routing_key = props.reply_to, properties = pika.BasicProperties(correlation_id = props.correlation_id), body = response)
    ch.basic_ack(delivery_tag = method.delivery_tag)


    print(f"[.] Done processing {n}")
    print(f"[.] Awaiting for requests")
    
channel.basic_qos(prefetch_count = 1)
channel.basic_consume(queue = queue_name, on_message_callback = on_request)
print("[.] Awaiting for requests")
channel.start_consuming()
