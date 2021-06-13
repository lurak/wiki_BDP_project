from kafka import KafkaConsumer
import sys
import time


if __name__ == "__main__":
    consumer = KafkaConsumer(
        "topic-1",
        bootstrap_servers=[sys.argv[1]]
    )
    lst = []

    start = time.time()
    for msg in consumer:
        print(msg.value)
