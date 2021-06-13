import os
import ast

from rest_framework.views import APIView
from rest_framework.views import Response
from google.cloud import storage


def init_bucket(dir_name):
    """
    Function to init bucket and read report
    :param dir_name: name of needed dir
    :return: data from report
    """
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './bigdataproject-316515-a0d5568146f9.json'
    client = storage.Client()
    bucket = client.get_bucket('bigdata-project-2021')
    stats = bucket.list_blobs()
    json_file = str()
    for stat in stats:
        if stat.name[:5] == dir_name and stat.name[-4:] == "json":
            json_file = stat.name
    blob = bucket.blob(json_file)
    data = blob.download_as_string()
    return data


def parse_data(data):
    """
    Parse data to list of jsons
    :param data: string with jsons
    :return: list of jsons
    """
    data = data.decode("UTF-8")
    data = data.split('\n')
    json_result = list()
    for row in data[:-1]:
        json_result.append(ast.literal_eval(row))
    return json_result


class WikiReportTopTwenty(APIView):
    """
    View to show 3 report(Return Top 20 users that created the most pages during the last 6 hours)
    """
    @staticmethod
    def get(request):
        """
        Get report
        :param request: request
        :return: Response
        """
        data = init_bucket("task3")
        json_result = parse_data(data)
        return Response({"report": json_result})


class WikiReportByHours(APIView):
    """
     View to show 1 report(Return the aggregated statistics containing the number of created pages
     for each Wikipedia domain for each hour in the last 6 hours)
    """
    @staticmethod
    def get(request):
        """
        Get report
        :param request: request
        :return: Response
        """
        data = init_bucket("task1")
        json_result = parse_data(data)
        return Response({"report": json_result})


class WikiReportBotSixHours(APIView):
    """
    View to show 2 report(Return the statistics about the number of pages
    created by bots for each of the domains for the last 6 hours)
    """
    @staticmethod
    def get(request):
        """
        Get report
        :param request: request
        :return: Response
        """
        data = init_bucket("task2")
        data = data.decode("UTF-8")
        json_data = ast.literal_eval(data)
        return Response(json_data)
