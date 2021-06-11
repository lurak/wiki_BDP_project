import pyspark
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
import json
import psycopg2


def add_to_db(message: pyspark.rdd.RDD, hostname=1,username=1, password=1, database=1):
    # print(type(message))
    # message.foreach(lambda x: print(x))
    new_mess = message.take(100000000)

    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)

    cursor = conn.cursor()

    for mess in new_mess:
        cursor.execute("insert into Page (page_id, page_name, created_at, user_id, domain_name) "
                       "values (%s, %s, %s, %s, %s, %s) ",
                       [mess["page_id"], mess["page_title"], mess["rev_timestamp"],
                        mess["user_id"], mess["meta"]["domain"]])

        conn.commit()
    conn.close()
    # new_message = message.take(1000000)


if __name__ == "__main__":
    sc = SparkContext("local[*]", "Wiki")
    sc.setLogLevel("ERROR")

    ssc = StreamingContext(sc, 5)
    kvs = KafkaUtils.createStream(ssc, "localhost:2181", "1", {"topic-1": 1})  # localhost:2181

    j = kvs.map(lambda x: json.loads(x[1]))
    j.foreachRDD(lambda x: add_to_db(x))


    ssc.start()
    ssc.awaitTermination()