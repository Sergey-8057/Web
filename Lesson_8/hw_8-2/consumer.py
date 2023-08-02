import pika, sys, os

from models import Contact


def main():
    credentials = pika.PlainCredentials('guest', 'guest')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
    channel = connection.channel()

    channel.queue_declare(queue='customer_queue', durable=True)

    def callback(ch, method, properties, body):
        pk = body.decode()
        contact = Contact.objects(id=pk, status=False).first()
        if contact:
            contact.update(set__status=True)
        print(f" [v] Done: {contact.fullname}, {contact.email}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='customer_queue', on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        sys.exit(0)
