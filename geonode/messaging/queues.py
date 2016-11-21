from kombu import Exchange, Queue

geonode_task_exchange = Exchange("geonode", type="fanout")
queue_geoserver_events = Queue("geoserver.events", geonode_task_exchange)
