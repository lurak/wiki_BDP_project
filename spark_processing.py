import pyspark
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from datetime import datetime
import json
import sys
import psycopg2


def add_to_db(message: pyspark.rdd.RDD, hostname="34.134.215.151",
              username='postgres', password='postgres',
              database='bigdataproject'):

    # message.foreach(lambda x: print(x))
    new_mess = message.take(100000000)
    print("Test!")
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    print("Test accepted!")
    cursor = conn.cursor()

    for mess in new_mess:
        try:
            k = None
            for i in range(len(mess["id"])):
                if "timestamp" in mess["id"][i]:
                    k = i
                    break
            if k is None:
                continue
            data1 = (mess["data"]["page_id"], mess["data"]["page_title"],
             datetime.fromtimestamp(mess["id"][k]["timestamp"] / 1000),
             mess["data"]["performer"]["user_id"],
             mess["data"]["meta"]["domain"])
            data2 = (
            mess["data"]["performer"]["user_id"],
            mess["data"]["performer"]["user_text"],
            mess["data"]["performer"]["user_is_bot"])


            cursor.execute(
                """
                insert into Pages_User (user_id, user_name, user_is_bot)
                           values (%s, %s, %s)
                           ON CONFLICT (user_id) DO NOTHING
                """,

                data2
              )
            cursor.execute("insert into Pages_Page (page_id, page_name, created_at, user_id, domain_name)"
                           "values (%s, %s, %s, %s, %s)",
                           data1)

            conn.commit()
        except KeyError as e:
            print(e)
            print(mess)

    conn.close()


def reduce_statistics(x, y):
    x["statistics"] += y["statistics"]
    x["time"] += y["time"]
    return x


def reduce_by_key(x, y):
    x["count"] += y["count"]
    return x


if __name__ == "__main__":
    sc = SparkContext("local[*]", "Wiki")
    sc.setLogLevel("ERROR")

    ssc = StreamingContext(sc, 15)
    kvs = KafkaUtils.createStream(ssc, sys.argv[1], "1", {"topic-1": 1})  # localhost:2181

    j = kvs.map(lambda x: json.loads(x[1])).foreachRDD(lambda x: add_to_db(x))
    ssc.start()
    ssc.awaitTermination()
