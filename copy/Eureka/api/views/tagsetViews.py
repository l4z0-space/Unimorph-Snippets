from rest_framework import status, generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from ..models import TagSet
from ..serializers import TagSetSerializer


class TagSetList(generics.ListCreateAPIView):
    queryset = TagSet.objects.all()
    serializer_class = TagSetSerializer
    filterset_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'features']

    def options(self, request):
        return Response(status=status.HTTP_200_OK,
                    headers={"Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Headers":
                                "access-control-allow-origin"})

class TagSetDetail(generics.RetrieveUpdateAPIView):
    queryset = TagSet.objects.all()
    serializer_class = TagSetSerializer
    lookup_field = 'name'
    
    def options(self, request, name):
        return Response(status=status.HTTP_200_OK,
                    headers={"Access-Control-Allow-Origin": "*",
                                "Access-Control-Allow-Headers":
                                "access-control-allow-origin"})