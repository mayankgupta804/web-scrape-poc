import pika


def get_rabbit_mq_channel():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', connection_attempts=5, heartbeat_interval=60))
    channel = connection.channel()
    channel.queue_declare(queue='links_queue', durable=True)
    return channel
