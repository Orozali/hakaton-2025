from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.authentication import JWTAuthentication


class SingleTokenAuthentication(JWTAuthentication):
    def authenticate(self, request):
        if request.headers.get(
                'Authorization'
        ) == 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNzcyOTAyLCJpYXQiOjE3NDAxNjgxMDIsImp0aSI6ImQyYmI2MGI2YmJkNDQxOTQ5ZDMzMjg2ZjQwM2EyNjFhIiwidXNlcl9pZCI6MX0.HgabOFp4bdgzGf0qnNa4oq48m6EvCm9nY3ZFEFs4l9I':
            return None, None
        return super().authenticate(request)


class SingleTokenPermission(BasePermission):
    def has_permission(self, request, view):
        token = request.headers.get('Authorization')
        if token == 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNzcyOTAyLCJpYXQiOjE3NDAxNjgxMDIsImp0aSI6ImQyYmI2MGI2YmJkNDQxOTQ5ZDMzMjg2ZjQwM2EyNjFhIiwidXNlcl9pZCI6MX0.HgabOFp4bdgzGf0qnNa4oq48m6EvCm9nY3ZFEFs4l9I':
            return True
        return False
