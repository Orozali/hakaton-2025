from rest_framework.response import Response
from rest_framework.views import APIView
import requests


class SearchApi(APIView):

    def get(self, request):
        base_url = 'https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json'

        query_params = request.GET.dict()

        response = requests.get(base_url, params=query_params)
        return Response(response.json())
