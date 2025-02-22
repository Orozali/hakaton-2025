import requests
from django.db.models import Q
from django.templatetags.i18n import language

from rest_framework.response import Response
from rest_framework.views import APIView

from course.models import Course


class SearchApi(APIView):

    def get(self, request):
        base_url = 'https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json'

        language_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

        query_params = request.GET.dict()
        toefl_ibt = query_params.get('toefl_ibt')
        toefl_pbt = query_params.get('toefl_pbt')
        ielts = query_params.get('ielts')
        cerf = query_params.get('cerf')
        gpa = query_params.get('GPA')

        filters = Q()

        if toefl_ibt:
            filters &= Q(toefl_ibt__gte=toefl_ibt)
        if toefl_pbt:
            filters &= Q(toefl_pbt__gte=toefl_pbt)
        if ielts:
            filters &= Q(ielts=ielts)
        if gpa:
            gpa = gpa.split(',')
            gpa_calc = float(gpa[1]) * 5 / float(gpa[0])
            filters &= Q(original_grade__gte=gpa_calc)

        if cerf in language_levels:
            allowed_levels = language_levels[: language_levels.index(cerf) + 1]
            filters &= Q(cerf__in=allowed_levels)

        courses = Course.objects.filter(filters)

        response = requests.get(base_url, params=query_params)

        course_list = response.json()['courses']
        responses = []
        if courses:
            for course in course_list:
                if courses.filter(course_id=course['id']).exists():
                    responses.append(course)
        else:
            return Response(course_list)
        return Response(responses)
