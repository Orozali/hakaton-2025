from django.urls import path

from users.api import RegisterAPI, LoginAPI

urlpatterns = [
    path('register/', RegisterAPI.as_view(), name='register'),
    # path('logout/', LogoutApi.as_view(), name='logout'),
    path('login/', LoginAPI.as_view(), name='login'),
]
