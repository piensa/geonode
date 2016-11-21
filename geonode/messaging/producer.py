from __future__ import with_statement

from geonode.settings import BROKER_URL
from queues import geonode_task_exchange

from kombu.common import maybe_declare
from kombu.pools import producers

if __name__ == "__main__":
    from kombu import BrokerConnection

    connection = BrokerConnection(BROKER_URL)

    with producers[connection].acquire(block=True) as producer:
        maybe_declare(geonode_task_exchange, producer.channel)

        payload = {"operation": "create", "content": "the object"}
        producer.publish(payload, exchange='geonode', serializer="json",
                         routing_key='ROUTING_KEY')

