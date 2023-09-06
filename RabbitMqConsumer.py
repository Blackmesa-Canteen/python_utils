import ssl

import pika

import argparse

from config import rabbitmq_user, rabbitmq_password, rabbitmq_broker_id, region, vhost


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


def receive_data(queue_name):
    """
        helper to receive message from remote rabbitmq
        :return: data
    """

    # SSL Context for TLS configuration of Amazon MQ for RabbitMQ
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    ssl_context.set_ciphers('ECDHE+AESGCM:!ECDSA')

    url = f"amqps://{rabbitmq_user}:{rabbitmq_password}@{rabbitmq_broker_id}.mq.{region}.amazonaws.com:5671/{vhost}"

    parameters = pika.URLParameters(url)
    parameters.ssl_options = pika.SSLOptions(context=ssl_context)

    connection = pika.BlockingConnection(parameters)

    channel = connection.channel()
    # channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback,
                          auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Receive data from a RabbitMQ queue.')
    parser.add_argument('queue_name',
                        type=str,
                        help='The name of the queue to consume data from.')
    args = parser.parse_args()

    receive_data(args.queue_name)
