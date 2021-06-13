from rest_framework.views import APIView
from rest_framework.views import Response

from .models import Page
from .serialize import PageDetailSerializer


class WikiPage(APIView):
    """
    View to show 4 ad-hoc query
    """
    @staticmethod
    def get(request, pk):
        """
        Get data
        :param request: request
        :param pk: index of page
        :return: Response
        """
        queryset = Page.get_page_by_id(pk)
        return Response(PageDetailSerializer(queryset, many=True).data)


class WikiDomains(APIView):
    """
    View to show 1 ad-hoc query
    """
    @staticmethod
    def get(request):
        """
        Get data
        :param request: request
        :return: Response
        """
        queryset = {"domains": Page.get_all_domains()}
        return Response(queryset)


class WikiUser(APIView):
    """
    View to show 2 ad-hoc query
    """
    @staticmethod
    def get(request, pk):
        """
        Get data
        :param request: request
        :param pk: index of user
        :return: Response
        """
        queryset = {"pages": Page.get_pages_by_user(pk)}
        return Response(queryset)


class WikiPagesByDomain(APIView):
    """
    View to show 3 ad-hoc query
    """
    @staticmethod
    def get(request, pk):
        """
        Get data
        :param request: request
        :param pk: name of domain
        :return: Response
        """
        queryset = {'number_of_pages': Page.get_number_of_articles(pk)}
        return Response(queryset)


class WikiUsersByTime(APIView):
    """
    View to show 5 ad-hoc query
    """
    @staticmethod
    def get(request, date_start, date_end):
        """
        Get data
        :param request: request
        :param date_start: start of data range
        :param date_end: end of data range
        :return: Response
        """
        queryset = {"users": Page.get_users_by_time(date_start, date_end)}
        return Response(queryset)
