from __future__ import with_statement

from geonode.settings import BROKER_URL
from kombu import BrokerConnection
from kombu.common import maybe_declare
from kombu.pools import producers
from queues import queue_email_events, queue_geoserver_events, queue_notifications_events

connection = BrokerConnection(BROKER_URL)


def send_email_producer(layer_uuid, user_id):
    with producers[connection].acquire(block=True) as producer:
        maybe_declare(queue_email_events, producer.channel)
        payload = {
            "layer_uuid": layer_uuid,
            "user_id": user_id

        }
        producer.publish(
            payload,
            exchange='geonode',
            serializer='json',
            routing_key='email'
        )


def geoserver_upload_layer(layer_id):
    with producers[connection].acquire(block=True) as producer:
        maybe_declare(queue_geoserver_events, producer.channel)

        payload = {"layer_id": layer_id}
        producer.publish(
            payload,
            exchange='geonode',
            serializer='json',
            routing_key='geoserver'
        )


def notifications_send(instance_id, app_label, model, created=None):
    with producers[connection].acquire(block=True) as producer:
        maybe_declare(queue_notifications_events, producer.channel)

        payload = {"instance_id": instance_id,
                   "app_label": app_label,
                   "model": model,
                   "created": created}
        producer.publish(
            payload,
            exchange='geonode',
            serializer='json',
            routing_key='notifications'
        )
