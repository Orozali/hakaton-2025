from django.urls import path
from course.api import SearchApi, GptApi

urlpatterns = [
    path('search/', SearchApi.as_view(), name='search'),
    path('gpt/', GptApi.as_view(), name='gpt'),
]

