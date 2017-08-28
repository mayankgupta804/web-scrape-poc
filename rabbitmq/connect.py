import pika


def get_rabbit_mq_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', connection_attempts=5))
    channel = connection.channel()
    channel.queue_declare(queue='task_queue', durable=True)
    return channel
