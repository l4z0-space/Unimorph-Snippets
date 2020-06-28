from django.http import Http404
from django.shortcuts import get_list_or_404
from django.core.exceptions import MultipleObjectsReturned
from rest_framework import status, generics, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from ..models import Lemma, Word
from ..serializers import LemmaSerializer, RelatedWordSerializer
from ..utils import getDimOptions, getFeatures


class LemmaList(generics.ListCreateAPIView):
    queryset = Lemma.objects.all()
    serializer_class = LemmaSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_fields = ['language', 'animacy', 'transivity', 'author', 'pos', 'date_updated']
    search_fields = ['name']

    def options(self, request):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})


class LemmaDetail(generics.RetrieveUpdateAPIView):
    queryset = Lemma.objects.all()
    serializer_class = LemmaSerializer
    lookup_field = 'name'

    def get_related_words(self, pk):
        try:
            related_words = Word.objects.filter(lemma=pk)
            return related_words
        except Word.DoesNotExist:
            return Http404

    def get_object(self):
        queryset = self.get_queryset()
        filter = {self.lookup_field: self.kwargs[self.lookup_field]}
        objs = get_list_or_404(queryset, **filter)
        return objs[0]
    
    def retrieve(self, request, name, format=None):
        lemma = self.get_object()
        serializer = LemmaSerializer(lemma)
        related_words = self.get_related_words(lemma.id)
        words = RelatedWordSerializer(related_words, many=True)
        lemma_data = serializer.data
        words_data = words.data
        for i in words_data:
            dims = getDimOptions(i['tagset'])
            i['tagset'] = getFeatures(i['tagset'])
            i['dimensions'] = dims
        lemma_data['related_words'] = words_data
        return Response(lemma_data,
                        headers={"Access-Control-Allow-Origin": "*"},
                        status=status.HTTP_200_OK)

    def options(self, request, name):
        return Response(status=status.HTTP_200_OK,
                        headers={"Access-Control-Allow-Origin": "*",
                                 "Access-Control-Allow-Headers":
                                 "access-control-allow-origin"})
