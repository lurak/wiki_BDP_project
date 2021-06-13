import json
import sys
from datetime import datetime, timedelta

from pyspark import SparkContext
from pyspark.sql import SparkSession


def reduce_by_key(x, y):
    x["number"] += y["number"]
    return x


def reduce_by_key_two(x, y):
    x["statistics"] += y["statistics"]
    return x


def reduce_by_key_three(x, y):
    x["page_titles"] += y["page_titles"]
    x["number_of_pages"] += 1
    return x


def reduce_one(x, y):
    x["statistics"] += y["statistics"]
    return x


if __name__ == "__main__":
    sc = SparkContext(
        master="local",
        appName="BigDataSpark"
    )
    current_date = datetime.strptime(sys.argv[1], "%Y-%m-%d/%H:%M:%S")

    upper_bound = (current_date - timedelta(hours=1)).replace(minute=0, second=0)
    lower_bound = upper_bound - timedelta(hours=6)

    print("---------------------------------------")
    print("|Date Bounds|")
    print(lower_bound, upper_bound)
    print("---------------------------------------")

    properties = {
        "driver": "org.postgresql.Driver",
        "user": "postgres",
        "password": "postgres",
        "host": "34.134.215.151",
        "db": "bigdataproject"
    }

    spark = SparkSession \
        .builder \
        .appName("BigDataProg") \
        .getOrCreate()
    df_options = spark.read \
        .format("jdbc") \
        .option("url", f'jdbc:postgresql://{properties["host"]}:5432/{properties["db"]}') \
        .option("driver", properties["driver"]) \
        .option("password", properties["password"]) \
        .option("user", properties["user"])
    df_user = \
        df_options.option("dbtable", 'pages_user').load()

    df_pages = \
        df_options.option("dbtable", 'pages_page').load()

    df = df_user.join(df_pages, on="user_id")
    all_df = df.rdd.filter(lambda x: lower_bound <= x["created_at"] <= upper_bound)

    task1 = all_df.map(lambda x: ((x["created_at"].hour, x["domain_name"]),
                                  {
                                      "start_time": str(x["created_at"].hour) + ":00",
                                      "end_time": str((x["created_at"] + timedelta(hours=1)).hour) + ":00",
                                      "number": 1
                                  })).reduceByKey(reduce_by_key). \
        map(lambda x: (x[0][0], {
            "start_time": x[1]["start_time"],
            "end_time": x[1]["end_time"],
            "statistics": [{x[0][1]: x[1]["number"]}]
    })).reduceByKey(reduce_by_key_two).map(lambda x: x[1])

    task2 = all_df.filter(lambda x: x["user_is_bot"]) \
        .map(lambda x: (x["domain_name"],
                        1)) \
        .reduceByKey(lambda x, y: x + y) \
        .map(lambda x: {
            "start_time": str(lower_bound.hour) + ':00',
            "end_time": str(upper_bound.hour) + ':00',
            "statistics": [
                {
                    "domain": x[0],
                    "created_by_bots": x[1]
                }
            ]
        }).reduce(reduce_one)

    task3 = all_df.map(lambda x: (x["user_id"], {
        "time_start": str(lower_bound.hour) + ":00",
        "time_end": str(upper_bound.hour) + ":00",
        "user_id": x["user_id"],
        "user_name": x["user_name"],
        "page_titles": [x["page_name"]],
        "number_of_pages": 1
    })).reduceByKey(reduce_by_key_three).map(lambda x: x[1]).sortBy(lambda x: -x["number_of_pages"]).take(20)

    results = spark.read.json(sc.parallelize([json.dumps(task1.collect())]))
    results.coalesce(1).write.format('json').mode("overwrite").save(sys.argv[2] + "/task1")
    results = spark.read.json(sc.parallelize([json.dumps(task2)]))
    results.coalesce(1).write.format('json').mode("overwrite").save(sys.argv[2] + "/task2")
    results = spark.read.json(sc.parallelize([json.dumps(task3)]))
    results.coalesce(1).write.format('json').mode("overwrite").save(sys.argv[2] + "/task3")

