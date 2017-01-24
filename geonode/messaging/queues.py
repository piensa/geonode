from kombu import Exchange, Queue

geonode_exchange = Exchange("testExchange", type="fanout", durable=False)

queue_all_events = Queue("broadcast", geonode_exchange, routing_key="#")
queue_email_events = Queue("email.events", geonode_exchange, routing_key="email")
queue_geoserver_msg = Queue("geoserver.msg", geonode_exchange, routing_key="testRouting")
queue_geoserver_events = Queue("geoserver.events", geonode_exchange, routing_key="geoserver")
queue_notifications_events = Queue("notifications.events", geonode_exchange, routing_key="notifications")

