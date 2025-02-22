import requests
from django.db.models import Q
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from config.settings import GPT_API_KEY

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
        gre = query_params.get('gre')
        uni_assist = query_params.get('uni_assist')

        filters = Q()

        if gre:
            filters &= Q(gre__gte=gre)
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

        if uni_assist:
            filters &= Q(uni_assist=uni_assist)

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


class GptApi(APIView):
    parser_classes = [JSONParser]

    def post(self, request):
        api_key = GPT_API_KEY
        url = 'https://api.openai.com/v1/chat/completions'

        query = request.data.get('text')
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": (
                            'Extract attributes from the following text and respond in the exact JSON format: '
                            '{"toefl_ibt": null, "toefl_pbt": null, "ielts": null, "cerf": null, "uni_assist": false, '
                            '"GPA": 0, "gre": null}.'
                            'Text: "%s". '
                            'The response should only include the attributes in JSON format, like this: '
                            '{"toefl_ibt": null, "toefl_pbt": null, "ielts": null, "cerf": B1, "uni_assist": false, '
                            '"GPA": null, "gre": null}.' % query
                    )
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            attributes_json = (
                response_data['choices'][0]['message']['content'])
            response_data = json.loads(attributes_json)
            attributes_json = response_data
            base_url = 'https://www2.daad.de/deutschland/studienangebote/international-programmes/api/solr/en/search.json'

            language_levels = ['A1', 'A2', 'B1', 'B2', 'C1', 'C2']

            toefl_ibt = attributes_json.get('toefl_ibt')
            toefl_pbt = attributes_json.get('toefl_pbt')
            ielts = attributes_json.get('ielts')
            cerf = attributes_json.get('cerf')
            gpa = attributes_json.get('GPA')
            gre = attributes_json.get('gre')
            uni_assist = attributes_json.get('uni_assist')

            filters = Q()

            if gre:
                filters &= Q(gre__gte=gre)
            if toefl_ibt:
                filters &= Q(toefl_ibt__gte=toefl_ibt)
            if toefl_pbt:
                filters &= Q(toefl_pbt__gte=toefl_pbt)
            if ielts:
                filters &= Q(ielts=ielts)
            if gpa:
                try:
                    gpa = gpa.split(',')
                    gpa_calc = float(gpa[1]) * 5 / float(gpa[0])
                    filters &= Q(original_grade__gte=gpa_calc)
                except:
                    filters &= Q(original_grade__gte=gpa)

            if cerf in language_levels:
                allowed_levels = language_levels[
                                 : language_levels.index(cerf) + 1]
                filters &= Q(cerf__in=allowed_levels)
            if uni_assist:
                filters &= Q(uni_assist=uni_assist)

            query_params = {'limit': 20}

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
        else:
            return Response(
                {
                    "error": f"Request failed with status code {response.status_code}",
                    "details": response.text
                }
            )
