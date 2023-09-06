import pika


def callback(ch, method, properties, body):
    print(f" [x] Received {body}")


def receive_data(queue_name):
    """
        helper to receive message from remote rabbitmq
        :return: data
    """
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host='b-d6c2e027-eebd-49a7-90b3-1c587949a894.mq.ca-central-1.amazonaws.com',
            port=5671,
            credentials=None,
        )
    )

    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback,
                          auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    receive_data('demo-queue')
