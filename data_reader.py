from kafka import KafkaProducer
from sseclient import SSEClient as EventSource
import requests
import json
import sys


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=[sys.argv[1]], value_serializer=lambda x: x.encode('utf-8')) #host:9092
    url = "https://stream.wikimedia.org/v2/stream/page-create"
    lst = []
    i = 20
    for event in EventSource(url):
        if i < 0:
            break
        if event.event == 'message':
            try:
                print(event.data)
                producer.send("topic-1", event.data)
                # event_data = json.loads(event.data)
                # lst.append(event_data)
                # print(event_data)
                # i -= 1
            except ValueError:
                pass
            # else:
            #     # filter out events, keep only article edits (mediawiki.recentchange stream)
            #     if event_data['type'] == 'edit':
            #         # construct valid json event
            #         event_to_send = construct_event(event_data, user_types)
            #
            #         producer.send('wikipedia-events', value=event_to_send)
    with open('example.json', 'w', encoding='utf-8') as f:
        json.dump(lst, f, indent=2)