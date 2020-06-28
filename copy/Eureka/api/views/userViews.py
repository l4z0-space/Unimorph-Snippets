from rest_framework import status, generics
from django.contrib.auth.models import User
from ..serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer