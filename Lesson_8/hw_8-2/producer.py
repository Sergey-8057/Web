from datetime import datetime
from faker import Faker
import json
import pika

from models import Contact

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='home_work-8', exchange_type='direct')
channel.queue_declare(queue='customer_queue', durable=True)
channel.queue_bind(exchange='home_work-8', queue='customer_queue')

fake = Faker()


def main():
    for _ in range(10):
        contact = Contact(fullname=fake.name(), email=fake.email()).save()
        channel.basic_publish(exchange='home_work-8', routing_key='customer_queue', body=str(contact.id).encode(),
                              properties=pika.BasicProperties(delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE))
        print(f" [x] Contact: {contact.fullname}, {contact.email}")
    connection.close()


if __name__ == '__main__':
    main()
