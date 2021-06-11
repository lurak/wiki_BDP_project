import pyspark
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from pyspark import SparkContext
import json
import psycopg2


def add_to_db(message: pyspark.rdd.RDD, hostname="34.94.182.239",
              username='pivotal', password='ZSf5rUAs0EEwr',
              database='pages'):

    # message.foreach(lambda x: print(x))
    new_mess = message.take(100000000)
    print("Test!")
    conn = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
    print("Test accepted!")
    cursor = conn.cursor()

    for mess in new_mess:
        try:

            data = [mess["page_id"], mess["page_title"], mess["rev_timestamp"],
                   mess["performer"]["user_id"], mess["meta"]["domain"]]
            cursor.execute("insert into Pages_Page (page_id, page_name, created_at, user_id, domain_name) "
                           "values (%s, %s, %s, %s, %s) ",
                           data)

            conn.commit()
        except Exception as e:
            print(e)
            print(mess)
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