#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))

channel = connection.channel()

channel.exchange_declare(exchange='testExchange',
                         type='fanout')

result = channel.queue_declare(queue='wayner')
import ipdb; ipdb.set_trace()

queue_name = result.method.queue
print queue_name
channel.queue_bind(exchange='testExchange',
                   queue="wayner")

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(callback,
                      queue="wayner",
                      no_ack=True)

channel.start_consuming()
