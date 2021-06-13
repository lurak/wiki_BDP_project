import pyspark
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
from datetime import datetime
import json
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
            data = (mess["data"]["page_id"], mess["data"]["page_title"],
             datetime.fromtimestamp(mess["id"][0]["timestamp"] / 1000),
                    mess["data"]["performer"]["user_id"],
             mess["data"]["meta"]["domain"], mess["data"]["performer"]["user_text"],
             mess["data"]["performer"]["user_is_bot"])

            cursor.execute("insert into Pages_Page (page_id, page_name, created_at, user_id, domain_name, "
                           "user_name, user_is_bot) "
                           "values (%s, %s, %s, %s, %s, %s, %s) ",
                           data)

            conn.commit()
        except KeyError as e:
            print(e)
            print(mess)

    conn.close()
    # new_message = message.take(1000000)


def reduce_statistics(x, y):
    x["statistics"] += y["statistics"]
    x["time"] += y["time"]
    return x


def reduce_by_key(x, y):
    x["count"] += y["count"]
    return x


def save_to_file(x):
    l = x.take(1)[0]
    print(l)


def k(x):
    # print(x)
    return json.loads(x[1])




if __name__ == "__main__":
    sc = SparkContext("local[*]", "Wiki")
    sc.setLogLevel("ERROR")

    ssc = StreamingContext(sc, 5)
    kvs = KafkaUtils.createStream(ssc, "localhost:2181", "1", {"topic-1": 1})  # localhost:2181

    j = kvs.map(lambda x: k(x)).foreachRDD(lambda x: add_to_db(x))
    # to_report = j.map(lambda x: (x["meta"]["domain"], {"count": 1,
    #                                                    "time": x["rev_timestamp"]}))\
    #     .window(5, 5)\
    #     .reduceByKey(reduce_by_key)\
    #     .map(lambda x: {"time": [x[1]["time"]], "statistics": [{x[0]: x[1]["count"]}]})\
    #     .reduce(reduce_statistics).pprint(10)
    # to_report.foreachRDD()
    ssc.start()
    ssc.awaitTermination()
