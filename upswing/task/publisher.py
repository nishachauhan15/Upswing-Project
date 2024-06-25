import pika
import json
import random
import time
from datetime import datetime

def publish_message():
    # Establish a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='test_queue')

    while True:
        status = random.randint(0, 6)
        message = {
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        channel.basic_publish(exchange='',
                              routing_key='test_queue',
                              body=json.dumps(message))
        print(f"Sent '{message}'")
        time.sleep(1)

    # Close the connection
    connection.close()

if __name__ == "__main__":
    publish_message()
