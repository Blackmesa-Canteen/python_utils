import json
import threading

import pika

rabbitmq_user = 'john123'
rabbitmq_password = '123456'
rabbitmq_host = 'localhost'
rabbitmq_port = 5674
vhost = 'demo-vhost'

def send_message(message, producer_id):
    """
    Helper to publish message to rabbitmq locally
    :param message: message body
    :param producer_id: id of the producer
    :return: None
    """
    url = f"amqp://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_host}:{rabbitmq_port}/{vhost}"

    parameters = pika.URLParameters(url)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    # channel.queue_declare(queue='demo-queue')

    # Add a field to mark the producer id in JSON payload
    message_with_id = json.dumps({"producer_id": producer_id, "message": message})

    channel.basic_publish(exchange='',
                          routing_key='demo-queue',
                          body=message_with_id.encode('utf-8'))  # Encode the string to bytes

    print(f"[x] Sent message from producer {producer_id}")

    connection.close()


def threaded_function(producer_id, num_messages=10):
    """
    Function to be run in threads. Sends num_messages messages.
    :param producer_id: id of the producer thread
    :param num_messages: number of messages to send
    :return: None
    """
    for i in range(num_messages):
        send_message(f"Hello World! from producer {producer_id}", producer_id)


if __name__ == '__main__':
    num_producers = 5  # Number of producer threads
    num_messages = 50  # Number of messages each producer will send

    threads = []
    for i in range(num_producers):
        thread = threading.Thread(target=threaded_function, args=(i, num_messages))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print('RabbitMQProducer.py')
