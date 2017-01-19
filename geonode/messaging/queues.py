from kombu import Exchange, Queue

geonode_exchange = Exchange("geonode", type="topic")

queue_all_events = Queue("broadcast", geonode_exchange, routing_key="#")
queue_email_events = Queue("email.events", geonode_exchange, routing_key="email")
queue_geoserver_events = Queue("geoserver.events", geonode_exchange, routing_key="geoserver")
queue_notifications_events = Queue("notifications.events", geonode_exchange, routing_key="notifications")
