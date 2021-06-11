from rest_framework.views import APIView
from rest_framework.views import Response
from .models import Page
from .serialize import PageDetailSerializer


class WikiPage(APIView):
    @staticmethod
    def get(request, pk):
        queryset = Page.get_page_by_id(pk)
        return Response(PageDetailSerializer(queryset, many=True).data)
