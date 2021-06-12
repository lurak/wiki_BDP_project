from rest_framework.views import APIView
from rest_framework.views import Response
from .models import Page
from .serialize import PageDetailSerializer


class WikiPage(APIView):
    @staticmethod
    def get(request, pk):
        queryset = Page.get_page_by_id(pk)
        return Response(PageDetailSerializer(queryset, many=True).data)


class WikiDomains(APIView):
    @staticmethod
    def get(request):
        queryset = {"domains": Page.get_all_domains()}
        return Response(queryset)


class WikiUser(APIView):
    @staticmethod
    def get(request, pk):
        queryset = {"pages": Page.get_pages_by_user(pk)}
        return Response(queryset)


class WikiPagesByDomain(APIView):
    @staticmethod
    def get(request, pk):
        queryset = {'number_of_pages': Page.get_number_of_articles(pk)}
        return Response(queryset)


class WikiUsersByTime(APIView):
    @staticmethod
    def get(request, date_start, date_end):
        print(date_start, date_end)
        queryset = {"users": Page.get_users_by_time(date_start, date_end)}
        return Response(queryset)
