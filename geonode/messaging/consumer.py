from geonode.geoserver.signals import geoserver_post_save2
from geonode.social.signals import notification_post_save_resource2
from queues import queue_geoserver_events, queue_notifications_events, queue_all_events
from kombu.mixins import ConsumerMixin


class Consumer(ConsumerMixin):
    def __init__(self, connection):
        self.connection = connection
        return

    def get_consumers(self, Consumer, channel):
        return [
            Consumer(queue_all_events,
                     callbacks=[self.on_message]),
            Consumer(queue_geoserver_events,
                     callbacks=[self.on_geoserver_messages]),
            Consumer(queue_notifications_events,
                     callbacks=[self.on_notifications_message]),
        ]

    def on_consume_end(self, connection, channel):
        super(Consumer, self).on_consume_end(connection, channel)
        print "Finished >>>"
        print channel

    def on_message(self, body, message):
        print ("broadcast: RECEIVED MSG - body: %r" % (body,))
        message.ack()
        return

    def on_geoserver_messages(self, body, message):
        print ("on_geoserver_messages: RECEIVED MSG - body: %r" % (body,))
        layer_id = body.get("layer_id")
        geoserver_post_save2(layer_id)
        message.ack()
        print ("on_geoserver_messages: finished")
        return

    def on_notifications_message(self, body, message):
        print ("on_notifications_message: RECEIVED MSG - body: %r" % (body,))
        instance_id = body.get("instance_id")
        app_label = body.get("app_label")
        model = body.get("model")
        created = body.get("created")
        notification_post_save_resource2(instance_id, app_label, model, created)
        message.ack()
        print ("on_notifications_message: finished")
        return

    def on_consume_ready(self, connection, channel, consumers, **kwargs):
        print ">>> Ready:"
        print connection
        print len(consumers), "consumers:"
        for i, consumer in enumerate(consumers, start=1):
            print i, consumer
        super(Consumer, self).on_consume_ready(connection, channel, consumers,
                                               **kwargs)