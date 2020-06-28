from rest_framework import filters
from django.shortcuts import get_list_or_404
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Feature
from ..serializers import FeatureSerializer

class FeatureList(generics.ListCreateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    filterset_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'dimension']
    
class FeatureDetail(generics.RetrieveUpdateAPIView):
    queryset = Feature.objects.all()
    serializer_class = FeatureSerializer
    lookup_field = 'name'
    
    def get_object(self):
        queryset = self.get_queryset()
        filter = {self.lookup_field: self.kwargs[self.lookup_field]}
        objs = get_list_or_404(queryset, **filter)
        return objs[0]
        