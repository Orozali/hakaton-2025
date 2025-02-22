from django.urls import path
from course.api import SearchApi

urlpatterns = [
    path('search/', SearchApi.as_view(), name='search'),
]

