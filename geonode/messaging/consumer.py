import logging
import sys

from geonode.geoserver.signals import geoserver_post_save2
from geonode.security.views import send_email_consumer
from geonode.social.signals import notification_post_save_resource2
from kombu.mixins import ConsumerMixin
from queues import queue_email_events, queue_geoserver_events, queue_notifications_events, queue_all_events

logger = logging.getLogger(__package__)
logger.addHandler(logging.StreamHandler(sys.stdout))
logger.setLevel(logging.DEBUG)

class Consumer(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection
        return

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(queue_all_events,
                     callbacks=[self.on_message]),
            Consumer(queue_email_events,
                     callbacks=[self.on_email_messages]),
            Consumer(queue_geoserver_events,
                     callbacks=[self.on_geoserver_messages]),
            Consumer(queue_notifications_events,
                     callbacks=[self.on_notifications_messages]),
        ]

    def on_consume_end(self, connection, channel):
        super(Consumer, self).on_consume_end(connection, channel)
        logger.info("finished.")
        print channel

    def on_message(self, body, message):
        logger.info("broadcast: RECEIVED MSG - body: %r" % (body,))
        message.ack()
        return

    def on_email_messages(self, body, message):
        logger.info("on_email_messages: RECEIVED MSG - body: %r" % (body,))
        layer_uuid = body.get("layer_uuid")
        user_id = body.get("user_id")
        send_email_consumer(layer_uuid, user_id)
        message.ack()
        logger.info("on_email_messages: finished")


    def on_geoserver_messages(self, body, message):
        logger.info("on_geoserver_messages: RECEIVED MSG - body: %r" % (body,))
        layer_id = body.get("layer_id")
        geoserver_post_save2(layer_id)
        message.ack()
        logger.info("on_geoserver_messages: finished")
        return

    def on_notifications_messages(self, body, message):
        logger.info("on_notifications_message: RECEIVED MSG - body: %r" % (body,))
        instance_id = body.get("instance_id")
        app_label = body.get("app_label")
        model = body.get("model")
        created = body.get("created")
        notification_post_save_resource2(instance_id, app_label, model, created)
        message.ack()
        logger.info("on_notifications_message: finished")
        return

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        logger.info(">>> Ready:")
        logger.info(connection)
        logger.info("{} consumers:".format(len(consumers)))
        for i, consumer in enumerate(consumers, start=1):
            logger.info("{0} {1}".format(i, consumer))

        super(Consumer, self).on_consume_ready(connection, channel, consumers,
                                               **kwargs)