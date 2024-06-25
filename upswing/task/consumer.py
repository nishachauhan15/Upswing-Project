import pika
import json
from pymongo import MongoClient

def insert_message_to_db(message):
    # Establish a connection with MongoDB
    client = MongoClient('localhost', 27017)
    db = client.test
    collection = db.mycollection

    # Insert the message into the collection
    collection.insert_one({"message": message})
    print(f"Inserted '{message}' into MongoDB")

def callback(ch, method, properties, body):
    message = body.decode()
    print(f"Received '{message}'")
    insert_message_to_db(json.loads(message))

def consume_message():
    # Establish a connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare a queue
    channel.queue_declare(queue='test_queue')

    # Set up subscription on the queue
    channel.basic_consume(queue='test_queue',
                          on_message_callback=callback,
                          auto_ack=True)

    print('Waiting for messages')
    channel.start_consuming()

if __name__ == "__main__":
    consume_message()
