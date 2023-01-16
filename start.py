#!/usr/bin/env python
import pika
import os 
import subprocess
import pika
import os
import time

from src.commands import *

#credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.environ["CENTRAL_SERVER_IP"], port=os.environ["CENTRAL_SERVER_PORT"], heartbeat=600, blocked_connection_timeout=300))

#pika.ConnectionParameters(
#   host=RABBIT_MQ_HOST, credentials=CREDENTIALS, heartbeat=0
#)

channel = connection.channel()
queue_name= os.environ["HOSPITAL_NAME"]
channel.queue_declare(queue=queue_name)

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
    print(f"[.] Received {n}") 
    try:
        response = eval(n)
        if response == None:
            response = f"Command not found {n}"
        print("RESPONSE:", response)
        ch.basic_publish(exchange='',
                        routing_key=props.reply_to,
                        properties=pika.BasicProperties(correlation_id = \
                                                            props.correlation_id),
                        body=response)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f" [x] Got error: {e}")
    print(f"[.] Done processing {n}")
    print(f"[.] Awaiting for requests")
    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue=queue_name, on_message_callback=on_request)
print("[.] Awaiting for requests")
channel.start_consuming()
