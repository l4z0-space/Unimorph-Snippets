from django.http import Http404
from rest_framework import status, generics
from ..models import Genus
from django_filters.rest_framework import DjangoFilterBackend
from ..serializers import GenusSerializer


class GenusList(generics.ListCreateAPIView):
    queryset = Genus.objects.all()
    serializer_class = GenusSerializer
    filterset_backends = [DjangoFilterBackend]
    filterset_fields = ['name']
    