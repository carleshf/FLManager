#!/usr/bin/env python
import pika
import argparse
import uuid
from pathlib import Path
from amqpstorm import management
import multiprocessing

hospital_list = [
"UB",
#"BUCH",
#"GEM",
#"ICRC",
#"KUH",
#"UCL",
#"UMCU",
#"AUMC",
#"VHIR",
]
mq_connection = "amqp://guest:guest@84.88.189.135:5672/%2F"
parameters = pika.URLParameters(mq_connection)

 # if mq_connection.startswith('amqps'):
 #     context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS)
 #     context.check_hostname = False

 #     cacertfile = Path('/home/user/LocalEGA/tests/_common/mq/CA.cert.pem')
 #     certfile   = Path('/home/user/LocalEGA/tests/_common/mq/testsuite.cert.pem')
 #     keyfile    = Path('/home/user/LocalEGA/tests/_common/mq/testsuite.sec.pem')

 #     context.verify_mode = ssl.CERT_NONE

 #     # Require server verification
 #     if cacertfile.exists():
 #         context.verify_mode = ssl.CERT_REQUIRED
 #         context.load_verify_locations(cafile=str(cacertfile))

 #     # If client verification is required
 #     if certfile.exists():
 #         assert( keyfile.exists() )
 #         context.load_cert_chain(str(certfile), keyfile=str(keyfile))

 #     # Finally, the pika ssl options
 #     parameters.ssl_options = pika.SSLOptions(context=context, server_hostname=None)

class RpcClient(object):

    def __init__(self):
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

        self.response = None
        self.corr_id = str(uuid.uuid4())

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self,n,hospital):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key= hospital,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(n))
        #connection.process_data_events() #this is blocking
        self.connection.process_data_events(time_limit=None)
        return self.response

def start_call(execute,hospital):
    try:
        rpc = RpcClient()
        print(f" [x] Requesting {execute} to {hospital}")
        response = rpc.call(execute,hospital)
        print(f" [.] RESPONSE FROM {hospital}: {response}")
    except Exception as e:
        print(f" [.] Got error: {e}")


if __name__ == '__main__':
    
    #get arguments from command line using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--function", help="function to call, default self_check", 
                        choices=['start_client', 'self_check', 'update_repo', 'update_image', 'stop_client'],
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

    execute = f"{function}('{argument}')"
    for hospital in hospital_list:
       #start process start_call
        p = multiprocessing.Process(target=start_call, args=(execute, hospital,))
        p.start()
