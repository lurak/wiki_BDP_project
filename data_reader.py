from kafka import KafkaProducer
from sseclient import SSEClient as EventSource
import sys


if __name__ == "__main__":
    producer = KafkaProducer(bootstrap_servers=[sys.argv[1]], value_serializer=lambda x: x.encode('utf-8')) #host:9092
    url = "https://stream.wikimedia.org/v2/stream/page-create"
    lst = []
    for event in EventSource(url):
        if event.event == 'message':
            try:
                data = '{"id":' + event.id + ',' + \
                              '"data": ' + event.data + '}'
                print(data)
                producer.send("topic-1", data)

            except Exception as e:
                print(e)
