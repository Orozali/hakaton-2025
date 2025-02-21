from django.urls import path, include

from config.drf_urls import urlpatterns as drf_urls

urlpatterns = [
    path('users/', include('users.urls')),
    path('course/', include('course.urls')),
]

urlpatterns += drf_urls